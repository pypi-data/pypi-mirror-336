from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError


def _get_kwargs(
    query_id: str,
    *,
    filter_: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    generate_schema: Optional[str] = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["filter"] = filter_

    params["offset"] = offset

    params["limit"] = limit

    params["generateSchema"] = generate_schema

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/executeAsyncQuery/{query_id}/results".format(
            query_id=query_id,
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
    query_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    filter_: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    generate_schema: Optional[str] = None,
) -> Response[Union[Any, DefaultError]]:
    """Get Query Execution Results

     Get the query execution results from Snowflake warehouse

    Args:
        query_id (str): The query statement’s unique execution ID
        filter_ (Optional[str]): Include additional conditions such as WHERE clauses and ORDER BY
            to refine the results. Example COLUMN_1='value' ORDER BY COLUMN_2 DESC
        offset (Optional[int]): The page number of resources to retrieve
        limit (Optional[int]): The number of resources to return in a given page
        generate_schema (Optional[str]): The schema generate button

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DefaultError]]
    """

    kwargs = _get_kwargs(
        query_id=query_id,
        filter_=filter_,
        offset=offset,
        limit=limit,
        generate_schema=generate_schema,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    query_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    filter_: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    generate_schema: Optional[str] = None,
) -> Optional[Union[Any, DefaultError]]:
    """Get Query Execution Results

     Get the query execution results from Snowflake warehouse

    Args:
        query_id (str): The query statement’s unique execution ID
        filter_ (Optional[str]): Include additional conditions such as WHERE clauses and ORDER BY
            to refine the results. Example COLUMN_1='value' ORDER BY COLUMN_2 DESC
        offset (Optional[int]): The page number of resources to retrieve
        limit (Optional[int]): The number of resources to return in a given page
        generate_schema (Optional[str]): The schema generate button

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DefaultError]
    """

    return sync_detailed(
        query_id=query_id,
        client=client,
        filter_=filter_,
        offset=offset,
        limit=limit,
        generate_schema=generate_schema,
    ).parsed


async def asyncio_detailed(
    query_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    filter_: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    generate_schema: Optional[str] = None,
) -> Response[Union[Any, DefaultError]]:
    """Get Query Execution Results

     Get the query execution results from Snowflake warehouse

    Args:
        query_id (str): The query statement’s unique execution ID
        filter_ (Optional[str]): Include additional conditions such as WHERE clauses and ORDER BY
            to refine the results. Example COLUMN_1='value' ORDER BY COLUMN_2 DESC
        offset (Optional[int]): The page number of resources to retrieve
        limit (Optional[int]): The number of resources to return in a given page
        generate_schema (Optional[str]): The schema generate button

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DefaultError]]
    """

    kwargs = _get_kwargs(
        query_id=query_id,
        filter_=filter_,
        offset=offset,
        limit=limit,
        generate_schema=generate_schema,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    query_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    filter_: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    generate_schema: Optional[str] = None,
) -> Optional[Union[Any, DefaultError]]:
    """Get Query Execution Results

     Get the query execution results from Snowflake warehouse

    Args:
        query_id (str): The query statement’s unique execution ID
        filter_ (Optional[str]): Include additional conditions such as WHERE clauses and ORDER BY
            to refine the results. Example COLUMN_1='value' ORDER BY COLUMN_2 DESC
        offset (Optional[int]): The page number of resources to retrieve
        limit (Optional[int]): The number of resources to return in a given page
        generate_schema (Optional[str]): The schema generate button

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DefaultError]
    """

    return (
        await asyncio_detailed(
            query_id=query_id,
            client=client,
            filter_=filter_,
            offset=offset,
            limit=limit,
            generate_schema=generate_schema,
        )
    ).parsed
