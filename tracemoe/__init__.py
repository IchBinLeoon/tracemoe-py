"""
MIT License

Copyright (c) 2021 IchBinLeoon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging
from typing import Optional, Dict, Any, Union, BinaryIO, List
from urllib.parse import urljoin

import aiohttp
from aiohttp import ContentTypeError

__author__ = 'IchBinLeoon'
__version__ = '1.0.2'

log = logging.getLogger(__name__)

BASE_URL = 'https://api.trace.moe/'


class TraceMoeException(Exception):
    pass


class BadRequest(TraceMoeException):
    def __init__(self, error: str):
        super().__init__(f'Image is malformed, or some params are incorrect: {error}')


class PaymentRequired(TraceMoeException):
    def __init__(self, error: str):
        super().__init__(f'Search quota or concurrency limit exceeded: {error}')


class Forbidden(TraceMoeException):
    def __init__(self, error: str):
        super().__init__(f'No permission to access: {error}')


class NotFound(TraceMoeException):
    def __init__(self, error: str):
        super().__init__(f'The requested resource is not found: {error}')


class MethodNotAllowed(TraceMoeException):
    def __init__(self, error: str):
        super().__init__(f'Wrong HTTP method used: {error}')


class TooManyRequests(TraceMoeException):
    def __init__(self, error: str):
        super().__init__(f'HTTP rate limit exceeded: {error}')


class InternalServerError(TraceMoeException):
    def __init__(self, error: str):
        super().__init__(f'Database error: {error}')


class ServiceUnavailable(TraceMoeException):
    def __init__(self, error: str):
        super().__init__(f'Database is overloaded: {error}')


class GatewayTimeout(TraceMoeException):
    def __init__(self, error: str):
        super().__init__(f'Database is not responding: {error}')


_exceptions = {
    400: BadRequest,
    402: PaymentRequired,
    403: Forbidden,
    404: NotFound,
    405: MethodNotAllowed,
    429: TooManyRequests,
    500: InternalServerError,
    503: ServiceUnavailable,
    504: GatewayTimeout
}


class TraceMoe:
    """Asynchronous wrapper client used to interact with the trace.moe API."""

    def __init__(self, session: Optional[aiohttp.ClientSession] = None, api_key: Optional[str] = None) -> None:
        """Initializes the trace.moe wrapper client.

        Args:
            session: An aiohttp session.
            api_key: A trace.moe API key.
        """
        self.session = session
        self.api_key = api_key

    async def __aenter__(self) -> 'TraceMoe':
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self.close()

    async def close(self) -> None:
        """Closes the aiohttp session."""
        if self.session is not None:
            await self.session.close()

    async def _session(self) -> aiohttp.ClientSession:
        """Gets an aiohttp session by creating it if it does not already exist."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def _request(self, method: str, *args, **kwargs) -> Dict[str, Any]:
        """Performs an HTTP request."""
        session = await self._session()
        response = await getattr(session, method)(*args, **kwargs)
        log.debug(f'{response.method} {response.url} {response.status} {response.reason}')
        if response.status != 200:
            exception = _exceptions[response.status]
            try:
                error = (await response.json()).get('error')
            except ContentTypeError:
                error = await response.text()
            raise exception(error)
        data = await response.json()
        return data

    async def search(
            self,
            image: Union[str, BinaryIO],
            cut_borders: Optional[bool] = False,
            anilist_id: Optional[int] = None,
            anilist_info: Optional[bool] = False,
    ) -> List[Dict[str, Any]]:
        """Searches the scene the anime screenshot is from by URL or upload.

        Args:
            image: The URL or file of the anime screenshot.
            cut_borders: Cut black borders.
            anilist_id: Filter by AniList ID.
            anilist_info: Include AniList info.

        Returns:
            The search results.

        Raises:
            TraceMoeException: If the API response contains an error.
        """
        params = {}
        data = None

        if isinstance(image, str):
            params['url'] = image
        else:
            data = {'image': image}

        if cut_borders is True:
            params['cutBorders'] = ''

        if anilist_id is not None:
            params['anilistID'] = anilist_id

        if anilist_info is True:
            params['anilistInfo'] = ''

        headers = {'x-trace-key': self.api_key} if self.api_key else None
        method = 'get' if data is None else 'post'

        url = urljoin(BASE_URL, 'search')
        data = await self._request(method, url=url, params=params, headers=headers, data=data)
        return data.get('result')

    async def me(self) -> Dict[str, Any]:
        """Checks the search quota and limit for your account (with API key) or IP address (without API key).

        Returns:
            The info about your account or IP address.

        Raises:
            TraceMoeException: If the API response contains an error.
        """
        url = urljoin(BASE_URL, 'me')
        data = await self._request('get', url=url)
        return data
