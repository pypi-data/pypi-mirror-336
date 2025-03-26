import logging
import os
from enum import Enum
from typing import Any, Dict, List

from httpx import AsyncClient, BasicAuth, Client, Response
from pydantic import BaseModel

from zmp_openapi_toolkit.models.mixed_spec import MixedAPISpecConfig
from zmp_openapi_toolkit.models.operation import ZmpAPIOperation
from zmp_openapi_toolkit.openapi.openapi_helper import OpenAPIHelper

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

_TIMEOUT = os.getenv("HTTPX_DEFAULT_TIMEOUT", 10)


class AuthenticationType(str, Enum):
    """Authentication type model"""

    NONE = "None"
    BASIC = "Basic"
    BEARER = "Bearer"
    ACCESS_KEY = "AccessKey"


class ZmpAPIWrapper:
    def __init__(
        self,
        server: str,
        /,
        *,
        headers: dict | None = None,
        cookies: dict | None = None,
        auth_type: AuthenticationType | None = AuthenticationType.NONE,
        username: str | None = None,
        password: str | None = None,
        bearer_token: str | None = None,
        access_key: str | None = None,
        tls_verify: bool | None = False,
        timeout: int | None = _TIMEOUT,
        mixed_api_spec_config: MixedAPISpecConfig,
    ):
        if not server:
            raise ValueError("Server URL is required")

        self._server = server
        self._headers = headers if headers is not None else {}
        self._cookies = cookies if cookies is not None else {}
        self._auth_type = auth_type
        self._username = username
        self._password = password
        self._bearer_token = bearer_token
        self._access_key = access_key
        self._tls_verify = tls_verify
        self._timeout = timeout

        self._auth = None
        self._client = None
        self._async_client = None

        self.openapi_helper = OpenAPIHelper(mixed_api_spec_config=mixed_api_spec_config)

        if self._headers.get("Content-Type") is None:
            self._headers.update({"Content-Type": "application/json"})

        if auth_type == AuthenticationType.BASIC:
            if not username or not password:
                raise ValueError(
                    "Username and password are required for Basic authentication"
                )
            self._auth = BasicAuth(username=username, password=password)

        elif auth_type == AuthenticationType.BEARER:
            if not bearer_token:
                raise ValueError("Bearer token is required for Bearer authentication")
            if self._bearer_token is not None:
                self._headers.update({"Authorization": f"Bearer {self._bearer_token}"})

        elif auth_type == AuthenticationType.ACCESS_KEY:
            if not access_key:
                raise ValueError("Access key is required for AccessKey authentication")
            if self._access_key is not None:
                self._headers.update({"X-Access-Key": f"{self._access_key}"})

    @property
    def async_client(self) -> AsyncClient:
        if self._async_client is None:
            self._async_client = AsyncClient(
                auth=self._auth,
                base_url=self._server,
                headers=self._headers,
                cookies=self._cookies,
                verify=self._tls_verify,
                timeout=self._timeout,
            )
        return self._async_client

    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = Client(
                auth=self._auth,
                base_url=self._server,
                headers=self._headers,
                cookies=self._cookies,
                verify=self._tls_verify,
                timeout=self._timeout,
            )
        return self._client

    async def close(self) -> None:
        """Close the async client."""
        if self._async_client is not None:
            await self._async_client.aclose()
            self._async_client = None

    def _get_response(self, response: Response) -> Dict[str, Any]:
        """Get response from API.

        Args:
            response (Response): Response from API

        Returns:
            Dict[str, Any]: Response data
        """
        if response.status_code == 200:
            logger.debug(f"Response: {response.json()}")

            return response.json()
        else:
            logger.warning(
                f"Failed to get response: {response.status_code} {response.text}"
            )
            return {
                "result": "failed",
                "code": response.status_code,
                "message": response.text,
            }

    def get_operations(self) -> List[ZmpAPIOperation]:
        return self.openapi_helper.generate_operations()

    def run(
        self,
        method: str,
        path: str,
        /,
        *,
        path_params: BaseModel | None = None,
        query_params: BaseModel | None = None,
        request_body: BaseModel | None = None,
    ) -> str:
        """Run the API request.

        Args:
            method (str): The HTTP method to use
            path (str): The path to the resource
            path_params (Any, optional): Path parameters for the tool. Defaults to None.
            query_params (Any, optional): Query parameters for the tool. Defaults to None.
            request_body (Any, optional): Request body for the tool. Defaults to None.

        Returns:
            str: Response from the API
        """
        logger.debug(f"Method: {method}, Path: {path}")
        logger.debug("-" * 100)
        logger.debug(f"Path params: {path_params}")
        logger.debug(f"Query params: {query_params}")
        logger.debug(f"Request body: {request_body}")

        if path_params is not None:
            # for path parameters
            # NOTE: exclude_none=True, mode="json" is used to exclude None values and convert to json (e.g. Enum values)
            path = path.format(**path_params.model_dump(exclude_none=True, mode="json"))

            logger.debug(f"Formatted path: {path}")

        logger.debug(
            f"Query params: {query_params.model_dump_json(exclude_none=True) if query_params else None}"
        )
        logger.debug(
            f"Request body: {request_body.model_dump_json(exclude_none=True) if request_body else None}"
        )

        # NOTE: If the request body is an array, we need to get the value for the array
        request_body_array_value = None
        if request_body:
            request_body_array_value = self._get_request_body_value_for_array(
                request_body
            )

        response = self.client.request(
            method,
            path,
            params=query_params.model_dump(exclude_none=True, mode="json")
            if query_params
            else None,
            json=request_body_array_value
            if request_body_array_value
            else request_body.model_dump(exclude_none=True, mode="json")
            if request_body
            else None,
        )

        response.raise_for_status()

        return self._get_response(response)

    def _get_request_body_value_for_array(
        self, request_body: BaseModel
    ) -> list[Any] | None:
        """Get request body value for array.

        Args:
            request_body (BaseModel): Request body

        Returns:
            Any: Request body value
        """
        request_body_value = None
        for i, (field_name, field_info) in enumerate(request_body.model_fields.items()):
            field_value = getattr(request_body, field_name)
            if i == 0 and field_value is not None:
                if isinstance(field_value, list):
                    request_body_value = [
                        item.model_dump(exclude_none=True, mode="json")
                        if isinstance(item, BaseModel)
                        else item
                        for item in field_value
                    ]
                    break
            else:
                logger.warning(f"Request body value is not array: {field_name}")
                return None

        logger.debug(f"Request body value: {request_body_value}")

        return request_body_value
