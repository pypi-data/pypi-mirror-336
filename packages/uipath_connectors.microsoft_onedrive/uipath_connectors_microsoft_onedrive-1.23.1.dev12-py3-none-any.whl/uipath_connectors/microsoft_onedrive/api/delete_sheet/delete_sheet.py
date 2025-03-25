from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError


def _get_kwargs(
    id: str,
    *,
    reference_id: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["referenceID"] = reference_id

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/DeleteSheet/{id}".format(
            id=id,
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
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    reference_id: str,
    reference_id_lookup: Any,
) -> Response[Union[Any, DefaultError]]:
    """Delete Sheet

     Deletes a specified sheet from workbook.

    Args:
        id (str): Sheet to delete from workbook
        reference_id (str): Workbook

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DefaultError]]
    """

    if not reference_id and reference_id_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get",
            url="/EventFolderPicker?includeFiles=true&onlyExcelFiles=true",
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if reference_id_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for reference_id_lookup in EventFolderPicker"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for reference_id_lookup in EventFolderPicker. Using the first match."
            )

        reference_id = found_items[0]["ReferenceID"]

    kwargs = _get_kwargs(
        id=id,
        reference_id=reference_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    reference_id: str,
    reference_id_lookup: Any,
) -> Optional[Union[Any, DefaultError]]:
    """Delete Sheet

     Deletes a specified sheet from workbook.

    Args:
        id (str): Sheet to delete from workbook
        reference_id (str): Workbook

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DefaultError]
    """

    return sync_detailed(
        id=id,
        client=client,
        reference_id=reference_id,
        reference_id_lookup=reference_id_lookup,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    reference_id: str,
    reference_id_lookup: Any,
) -> Response[Union[Any, DefaultError]]:
    """Delete Sheet

     Deletes a specified sheet from workbook.

    Args:
        id (str): Sheet to delete from workbook
        reference_id (str): Workbook

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DefaultError]]
    """

    if not reference_id and reference_id_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get",
            url="/EventFolderPicker?includeFiles=true&onlyExcelFiles=true",
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if reference_id_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for reference_id_lookup in EventFolderPicker"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for reference_id_lookup in EventFolderPicker. Using the first match."
            )

        reference_id = found_items[0]["ReferenceID"]

    kwargs = _get_kwargs(
        id=id,
        reference_id=reference_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    reference_id: str,
    reference_id_lookup: Any,
) -> Optional[Union[Any, DefaultError]]:
    """Delete Sheet

     Deletes a specified sheet from workbook.

    Args:
        id (str): Sheet to delete from workbook
        reference_id (str): Workbook

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DefaultError]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            reference_id=reference_id,
            reference_id_lookup=reference_id_lookup,
        )
    ).parsed
