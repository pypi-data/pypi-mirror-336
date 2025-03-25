from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError


def _get_kwargs(
    entity: str = "",
    *,
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    expand: Optional[str] = None,
    filter_: Optional[str] = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["pageSize"] = page_size

    params["nextPage"] = next_page

    params["$expand"] = expand

    params["$filter"] = filter_

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/entity/{entity}".format(
            entity=entity,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, DefaultError]]:
    if response.status_code == 200:
        response_200 = cast(Any, None)
        return response_200
    if response.status_code == 400:
        response_400 = DefaultError.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = DefaultError.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = DefaultError.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = DefaultError.from_dict(response.json())

        return response_404
    if response.status_code == 405:
        response_405 = DefaultError.from_dict(response.json())

        return response_405
    if response.status_code == 406:
        response_406 = DefaultError.from_dict(response.json())

        return response_406
    if response.status_code == 409:
        response_409 = DefaultError.from_dict(response.json())

        return response_409
    if response.status_code == 415:
        response_415 = DefaultError.from_dict(response.json())

        return response_415
    if response.status_code == 500:
        response_500 = DefaultError.from_dict(response.json())

        return response_500
    if response.status_code == 402:
        response_402 = DefaultError.from_dict(response.json())

        return response_402
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, DefaultError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    entity_lookup: Any,
    entity: str = "",
    *,
    client: Union[AuthenticatedClient, Client],
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    expand: Optional[str] = None,
    filter_: Optional[str] = None,
) -> Response[Union[Any, DefaultError]]:
    """List All Entity Records

     List all records for a entity

    Args:
        entity (str): Entity Default: ''.
        page_size (Optional[int]): The number of resources to return in a given page
        next_page (Optional[str]): The next page cursor, taken from the response header:
            `elements-next-page-token`
        expand (Optional[str]): Expand related entities
        filter_ (Optional[str]): Filter items by property values

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DefaultError]]
    """

    if not entity and entity_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/entity_dtl"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if entity_lookup in item["name"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for entity_lookup in entity_dtl")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for entity_lookup in entity_dtl. Using the first match."
            )

        entity = found_items[0]["value"]

    kwargs = _get_kwargs(
        entity=entity,
        page_size=page_size,
        next_page=next_page,
        expand=expand,
        filter_=filter_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    entity_lookup: Any,
    entity: str = "",
    *,
    client: Union[AuthenticatedClient, Client],
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    expand: Optional[str] = None,
    filter_: Optional[str] = None,
) -> Optional[Union[Any, DefaultError]]:
    """List All Entity Records

     List all records for a entity

    Args:
        entity (str): Entity Default: ''.
        page_size (Optional[int]): The number of resources to return in a given page
        next_page (Optional[str]): The next page cursor, taken from the response header:
            `elements-next-page-token`
        expand (Optional[str]): Expand related entities
        filter_ (Optional[str]): Filter items by property values

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DefaultError]
    """

    return sync_detailed(
        entity=entity,
        entity_lookup=entity_lookup,
        client=client,
        page_size=page_size,
        next_page=next_page,
        expand=expand,
        filter_=filter_,
    ).parsed


async def asyncio_detailed(
    entity_lookup: Any,
    entity: str = "",
    *,
    client: Union[AuthenticatedClient, Client],
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    expand: Optional[str] = None,
    filter_: Optional[str] = None,
) -> Response[Union[Any, DefaultError]]:
    """List All Entity Records

     List all records for a entity

    Args:
        entity (str): Entity Default: ''.
        page_size (Optional[int]): The number of resources to return in a given page
        next_page (Optional[str]): The next page cursor, taken from the response header:
            `elements-next-page-token`
        expand (Optional[str]): Expand related entities
        filter_ (Optional[str]): Filter items by property values

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DefaultError]]
    """

    if not entity and entity_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/entity_dtl"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if entity_lookup in item["name"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for entity_lookup in entity_dtl")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for entity_lookup in entity_dtl. Using the first match."
            )

        entity = found_items[0]["value"]

    kwargs = _get_kwargs(
        entity=entity,
        page_size=page_size,
        next_page=next_page,
        expand=expand,
        filter_=filter_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    entity_lookup: Any,
    entity: str = "",
    *,
    client: Union[AuthenticatedClient, Client],
    page_size: Optional[int] = None,
    next_page: Optional[str] = None,
    expand: Optional[str] = None,
    filter_: Optional[str] = None,
) -> Optional[Union[Any, DefaultError]]:
    """List All Entity Records

     List all records for a entity

    Args:
        entity (str): Entity Default: ''.
        page_size (Optional[int]): The number of resources to return in a given page
        next_page (Optional[str]): The next page cursor, taken from the response header:
            `elements-next-page-token`
        expand (Optional[str]): Expand related entities
        filter_ (Optional[str]): Filter items by property values

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DefaultError]
    """

    return (
        await asyncio_detailed(
            entity=entity,
            entity_lookup=entity_lookup,
            client=client,
            page_size=page_size,
            next_page=next_page,
            expand=expand,
            filter_=filter_,
        )
    ).parsed
