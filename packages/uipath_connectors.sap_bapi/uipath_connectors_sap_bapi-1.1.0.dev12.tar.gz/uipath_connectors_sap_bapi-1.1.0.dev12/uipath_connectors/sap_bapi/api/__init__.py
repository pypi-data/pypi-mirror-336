from .bapisexecute import (
    execute_bapi as _execute_bapi,
    execute_bapi_async as _execute_bapi_async,
)
from ..models.default_error import DefaultError
from typing import cast

from pydantic import Field
from typing import Any, Optional, Union

from ..client import Client
import httpx


class SapBapi:
    def __init__(self, *, instance_id: str, client: httpx.Client):
        base_url = str(client.base_url).rstrip("/")
        new_headers = {
            k: v for k, v in client.headers.items() if k not in ["content-type"]
        }
        new_client = httpx.Client(
            base_url=base_url + f"/elements_/v3/element/instances/{instance_id}",
            headers=new_headers,
            timeout=100,
        )
        new_client_async = httpx.AsyncClient(
            base_url=base_url + f"/elements_/v3/element/instances/{instance_id}",
            headers=new_headers,
            timeout=100,
        )
        self.client = (
            Client(
                base_url="",  # this will be overridden by the base_url in the Client constructor
            )
            .set_httpx_client(new_client)
            .set_async_httpx_client(new_client_async)
        )

    def execute_bapi(
        self,
        *,
        bapi_name: str,
        bapi_name_lookup: Any,
    ) -> Optional[Union[Any, DefaultError]]:
        return _execute_bapi(
            client=self.client,
            bapi_name=bapi_name,
            bapi_name_lookup=bapi_name_lookup,
        )

    async def execute_bapi_async(
        self,
        *,
        bapi_name: str,
        bapi_name_lookup: Any,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _execute_bapi_async(
            client=self.client,
            bapi_name=bapi_name,
            bapi_name_lookup=bapi_name_lookup,
        )
