# This file was auto-generated by Fern from our API Definition.

from ..core.client_wrapper import SyncClientWrapper
import typing
from ..core.request_options import RequestOptions
from ..types.customer_response import CustomerResponse
from ..core.pydantic_utilities import parse_obj_as
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper


class CustomerClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get(self, *, request_options: typing.Optional[RequestOptions] = None) -> CustomerResponse:
        """
        Get the account information associated with the API key.

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        CustomerResponse
            Look up success

        Examples
        --------
        from groundx import GroundX

        client = GroundX(
            api_key="YOUR_API_KEY",
        )
        client.customer.get()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/customer",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    CustomerResponse,
                    parse_obj_as(
                        type_=CustomerResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncCustomerClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def get(self, *, request_options: typing.Optional[RequestOptions] = None) -> CustomerResponse:
        """
        Get the account information associated with the API key.

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        CustomerResponse
            Look up success

        Examples
        --------
        import asyncio

        from groundx import AsyncGroundX

        client = AsyncGroundX(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.customer.get()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/customer",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    CustomerResponse,
                    parse_obj_as(
                        type_=CustomerResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
