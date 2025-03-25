from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.upload_files_body import UploadFilesBody
from ...models.upload_files_response import UploadFilesResponse


def _get_kwargs(
    *,
    body: UploadFilesBody,
    convert: Optional[bool] = None,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["convert"] = convert

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/hubs/general/upload_file",
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, UploadFilesResponse]]:
    if response.status_code == 200:
        response_200 = UploadFilesResponse.from_dict(response.json())

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
) -> Response[Union[DefaultError, UploadFilesResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadFilesBody,
    convert: Optional[bool] = None,
) -> Response[Union[DefaultError, UploadFilesResponse]]:
    """Upload Files

     Uploads files to google drive

    Args:
        convert (Optional[bool]): Whether to convert this file to the corresponding Google Docs
            Editors format
        body (UploadFilesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, UploadFilesResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
        convert=convert,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadFilesBody,
    convert: Optional[bool] = None,
) -> Optional[Union[DefaultError, UploadFilesResponse]]:
    """Upload Files

     Uploads files to google drive

    Args:
        convert (Optional[bool]): Whether to convert this file to the corresponding Google Docs
            Editors format
        body (UploadFilesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, UploadFilesResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
        convert=convert,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadFilesBody,
    convert: Optional[bool] = None,
) -> Response[Union[DefaultError, UploadFilesResponse]]:
    """Upload Files

     Uploads files to google drive

    Args:
        convert (Optional[bool]): Whether to convert this file to the corresponding Google Docs
            Editors format
        body (UploadFilesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, UploadFilesResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
        convert=convert,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadFilesBody,
    convert: Optional[bool] = None,
) -> Optional[Union[DefaultError, UploadFilesResponse]]:
    """Upload Files

     Uploads files to google drive

    Args:
        convert (Optional[bool]): Whether to convert this file to the corresponding Google Docs
            Editors format
        body (UploadFilesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, UploadFilesResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            convert=convert,
        )
    ).parsed
