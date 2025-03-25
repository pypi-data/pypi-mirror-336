from .entity import (
    list_all_entity_records as _list_all_entity_records,
    list_all_entity_records_async as _list_all_entity_records_async,
)
from ..models.default_error import DefaultError
from typing import cast

from pydantic import Field
from typing import Any, Optional, Union

from ..client import Client
import httpx


class SapOdata:
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

    def list_all_entity_records(
        self,
        entity_lookup: Any,
        entity: str = "",
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        expand: Optional[str] = None,
        filter_: Optional[str] = None,
    ) -> Optional[Union[Any, DefaultError]]:
        return _list_all_entity_records(
            client=self.client,
            entity=entity,
            entity_lookup=entity_lookup,
            page_size=page_size,
            next_page=next_page,
            expand=expand,
            filter_=filter_,
        )

    async def list_all_entity_records_async(
        self,
        entity_lookup: Any,
        entity: str = "",
        *,
        page_size: Optional[int] = None,
        next_page: Optional[str] = None,
        expand: Optional[str] = None,
        filter_: Optional[str] = None,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _list_all_entity_records_async(
            client=self.client,
            entity=entity,
            entity_lookup=entity_lookup,
            page_size=page_size,
            next_page=next_page,
            expand=expand,
            filter_=filter_,
        )
