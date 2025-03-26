import asyncio
from copy import deepcopy
import logging

import aiohttp
from requests.auth import HTTPBasicAuth

from fraudcrawler.common.settings import MAX_RETRIES, RETRY_DELAY

logger = logging.getLogger(__name__)


class ZyteApi:
    """A client to interact with the Zyte API for fetching product details."""

    _endpoint = "https://api.zyte.com/v1/extract"
    _config = {
        "javascript": False,
        "browserHtml": False,
        "screenshot": False,
        "productOptions": {"extractFrom": "httpResponseBody"},
        "httpResponseBody": True,
        "geolocation": "CH",
        "viewport": {"width": 1280, "height": 1080},
        "actions": [],
        "product": True,
    }

    def __init__(
        self,
        api_key: str,
        max_retries: int = MAX_RETRIES,
        retry_delay: int = RETRY_DELAY,
    ):
        """Initializes the ZyteApiClient with the given API key and retry configurations.

        Args:
            api_key: The API key for Zyte API.
            max_retries: Maximum number of retries for API calls.
            retry_delay: Delay between retries in seconds.
        """
        self._http_basic_auth = HTTPBasicAuth(api_key, "")
        self._aiohttp_basic_auth = aiohttp.BasicAuth(api_key)
        self._max_retries = max_retries
        self._retry_delay = retry_delay

    async def get_details(
        self, queue_in: asyncio.Queue, queue_out: asyncio.Queue
    ) -> None:
        """Fetches product details from the URLs in the queue_in using Zyte API and puts the results into queue_out.

        Args:
            queue_in: The input queue containing URLs to fetch product details from.
            queue_out: The output queue to put the product details as dictionaries.
        """
        while True:
            url = await queue_in.get()
            if url is None:
                queue_in.task_done()
                break

            try:
                product = await self._get_details_for_url(url=url)
                await queue_out.put(product)
            except Exception as e:
                logger.warning(f"Ignoring product from URL {url} due to error: {e}.")
            queue_in.task_done()

    async def _get_details_for_url(self, url: str) -> dict:
        """Helper coroutine to fetch product details for a single URL using aiohttp.

        Args:
            url: The URL to fetch product details from.
        """
        logger.info(f"Fetching product details by Zyte for URL {url}.")
        attempts = 0
        err = None
        while attempts < self._max_retries:
            try:
                logger.debug(
                    f"Fetch product details for URL {url} (Attempt {attempts + 1})."
                )
                product = await self._aiohttp_api_request(url=url)
                product["url"] = url
                return product
            except Exception as e:
                logger.debug(
                    f"Exception occurred while fetching product details for URL {url} (Attempt {attempts + 1})."
                )
                err = e
            attempts += 1
            if attempts < self._max_retries:
                await asyncio.sleep(self._retry_delay)
        if err is not None:
            raise err

    async def _aiohttp_api_request(self, url: str) -> dict:
        """Get the content of a given URL by an aiohttp post request to Zyte API."""

        # Prepare the request
        config = deepcopy(self._config)
        config["url"] = url

        # Perform the async request to Zyte API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=self._endpoint,
                json=config,
                auth=self._aiohttp_basic_auth,
            ) as response:
                response.raise_for_status()
                json_ = await response.json()
        return json_
