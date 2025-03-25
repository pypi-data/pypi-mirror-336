from .execute_async_query import (
    execute_async_query as _execute_async_query,
    execute_async_query_async as _execute_async_query_async,
)
from ..models.default_error import DefaultError
from ..models.execute_async_query_request import ExecuteAsyncQueryRequest
from ..models.execute_async_query_response import ExecuteAsyncQueryResponse
from typing import cast
from .execute_query import (
    execute_query as _execute_query,
    execute_query_async as _execute_query_async,
)
from ..models.execute_query_request import ExecuteQueryRequest
from .query_execution_results import (
    get_query_execution_results as _get_query_execution_results,
    get_query_execution_results_async as _get_query_execution_results_async,
)
from .query_execution_status import (
    get_query_execution_status as _get_query_execution_status,
    get_query_execution_status_async as _get_query_execution_status_async,
)
from ..models.get_query_execution_status_response import GetQueryExecutionStatusResponse

from pydantic import Field
from typing import Any, Optional, Union

from ..client import Client
import httpx


class SnowflakeSnowflake:
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

    def execute_async_query(
        self,
        *,
        body: ExecuteAsyncQueryRequest,
    ) -> Optional[Union[DefaultError, ExecuteAsyncQueryResponse]]:
        return _execute_async_query(
            client=self.client,
            body=body,
        )

    async def execute_async_query_async(
        self,
        *,
        body: ExecuteAsyncQueryRequest,
    ) -> Optional[Union[DefaultError, ExecuteAsyncQueryResponse]]:
        return await _execute_async_query_async(
            client=self.client,
            body=body,
        )

    def execute_query(
        self,
        *,
        body: ExecuteQueryRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return _execute_query(
            client=self.client,
            body=body,
        )

    async def execute_query_async(
        self,
        *,
        body: ExecuteQueryRequest,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _execute_query_async(
            client=self.client,
            body=body,
        )

    def get_query_execution_results(
        self,
        query_id: str,
        *,
        filter_: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        generate_schema: Optional[str] = None,
    ) -> Optional[Union[Any, DefaultError]]:
        return _get_query_execution_results(
            client=self.client,
            query_id=query_id,
            filter_=filter_,
            offset=offset,
            limit=limit,
            generate_schema=generate_schema,
        )

    async def get_query_execution_results_async(
        self,
        query_id: str,
        *,
        filter_: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        generate_schema: Optional[str] = None,
    ) -> Optional[Union[Any, DefaultError]]:
        return await _get_query_execution_results_async(
            client=self.client,
            query_id=query_id,
            filter_=filter_,
            offset=offset,
            limit=limit,
            generate_schema=generate_schema,
        )

    def get_query_execution_status(
        self,
        query_id: str,
    ) -> Optional[Union[DefaultError, GetQueryExecutionStatusResponse]]:
        return _get_query_execution_status(
            client=self.client,
            query_id=query_id,
        )

    async def get_query_execution_status_async(
        self,
        query_id: str,
    ) -> Optional[Union[DefaultError, GetQueryExecutionStatusResponse]]:
        return await _get_query_execution_status_async(
            client=self.client,
            query_id=query_id,
        )
