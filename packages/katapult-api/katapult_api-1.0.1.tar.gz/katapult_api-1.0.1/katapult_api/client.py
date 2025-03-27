import asyncio
import logging.config
from time import time
from typing import Any, Literal, Optional

import aiohttp

from .structs import Response

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, base_url: str, api_key: str, concurrent_rate_limit: int) -> None:
        self._base_url = base_url
        self._root_params = {
            "api_key": api_key
        }  # todo this is probably more katapult specific
        self._session: aiohttp.ClientSession | None = None
        self._semaphore = asyncio.Semaphore(value=concurrent_rate_limit)

        self._task_id = 0

    def _clean_params(self, params: dict[str, Any]) -> dict:
        # used to remove none items
        return {k: v for k, v in params.items() if v}

    async def request(
        self,
        method: Literal["GET", "POST", "PUT", "DEL", "PATCH"],
        url: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> Response:
        if self._session:
            try:
                if params:
                    params = self._clean_params(params)
                else:
                    params = {}

                # add api key to params (according to the katapult pro docs it gets sent as a query param in each request)
                params.update(self._root_params)

                response = Response(self._task_id, time())
                self._task_id += 1

                # todo this might be kinda limiting but this is just for debugging so idk right now
                logger.debug(f"Task ({response.id:0>6}): {method} {url}")

                async with self._semaphore:
                    content, headers, status = await self._request(
                        method=method, url=url, params=params, json=json
                    )

                response.end = time()
                response.content = content
                response.url = url
                response.headers = headers
                response.method = method
                response.status = status

                logger.debug(
                    f"Task ({response.id:0>6}): {method} {url.split('?')[0]} returned {status} in {response.end - response.start:.2f}s"
                )

                return response
            except Exception as e:
                logger.critical("Uncaught error!", exc_info=True)
                raise e
        else:
            raise Exception(
                "aiohttp session has not begun!"
            )  # todo maybe a custom exception or see if aiohttp has one

    async def _request(
        self,
        method: Literal["GET", "POST", "PUT", "DEL", "PATCH"],
        url: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> tuple[str, dict, int]:
        async with self._session.request(
            method, url, params=params, json=json
        ) as client_response:
            content = await client_response.text()

            return (
                content,
                dict(client_response.headers),
                client_response.status,
            )

    async def __aenter__(self, *args, **kwargs) -> "Client":
        self._session = aiohttp.ClientSession(*args, **kwargs)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()
            self._session = None
            self._task_id = 0

    def __repr__(self):
        return f"{self._base_url},{self._root_params}"
