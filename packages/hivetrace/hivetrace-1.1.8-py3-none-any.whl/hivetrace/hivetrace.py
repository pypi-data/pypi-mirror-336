import os
from typing import Dict, Any, Optional, Union
import uuid

import httpx
import asyncio
from dotenv import load_dotenv
import asyncio
import functools


class MissingConfigError(Exception):
    def __init__(self, param: str):
        super().__init__(f"Config parameter '{param}' is missing")


class InvalidParameterError(Exception):
    pass


class UnauthorizedError(Exception):
    def __init__(self, message="Invalid or expired access token"):
        super().__init__(message)


class HivetraceSDK:
    def __init__(
        self, config: Optional[Dict[str, Any]] = None, async_mode: bool = True
    ) -> None:
        self.config = config or self._load_config_from_env()
        self.hivetrace_url = self._get_required_config("HIVETRACE_URL")
        self.hivetrace_access_token = self._get_required_config(
            "HIVETRACE_ACCESS_TOKEN"
        )
        self.async_mode = async_mode

        self.session = httpx.AsyncClient() if async_mode else httpx.Client()


    def _handle_http_error(self, e: httpx.HTTPStatusError) -> Dict[str, Any]:
        return {
            "error": f"HTTP error {e.response.status_code}: {e.response.text}",
            "status_code": e.response.status_code,
        }
    

    def _handle_request_error(self, e: httpx.RequestError, application_id: str) -> Dict[str, Any]:
        return {
            "error": f"Request error while contacting API: {str(e)}",
            "application_id": application_id,
        }


    def _load_config_from_env(self) -> Dict[str, Any]:
        return {
            "HIVETRACE_URL": os.getenv("HIVETRACE_URL", "").strip(),
            "HIVETRACE_ACCESS_TOKEN": os.getenv("HIVETRACE_ACCESS_TOKEN", "").strip(),
        }


    def _get_required_config(self, key: str) -> str:
        value = self.config.get(key, "").strip()
        if not value:
            raise MissingConfigError(key)
        return value.rstrip("/")


    @staticmethod
    def _validate_application_id(application_id: str) -> str:
        try:
            return str(uuid.UUID(application_id))
        except ValueError as e:
            raise InvalidParameterError("Invalid application_id format") from e


    @staticmethod
    def _validate_message(message: str) -> None:
        if not isinstance(message, str) or not message.strip():
            raise InvalidParameterError("Message must be non-empty")


    @staticmethod
    def _validate_additional_parameters(
        additional_parameters: Optional[Dict[str, Any]]
    ) -> None:
        if additional_parameters is not None and not isinstance(additional_parameters, dict):
            raise InvalidParameterError("Additional parameters must be a dict or None")

    async def _send_request_async(
        self, endpoint: str, payload: Dict[str, Any]
    ) -> None:
        """Fire-and-forget: Sends request asynchronously but does not wait for response."""
        url = f"{self.hivetrace_url}/{endpoint.lstrip('/')}"
        headers = {"Authorization": f"Bearer {self.hivetrace_access_token}"}
        try:
            await self.session.post(url, json=payload, headers=headers)
        except Exception as e:
            print(
                f"Async request failed: {e}"
            )  # Log error but don't block execution

    def _send_request_sync(
        self, endpoint: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Sends request synchronously and waits for the response."""
        url = f"{self.hivetrace_url}/{endpoint.lstrip('/')}"
        headers = {"Authorization": f"Bearer {self.hivetrace_access_token}"}
        try:
            response = self.session.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"HTTP error {e.response.status_code}: {e.response.text}"
            }
        except httpx.RequestError as e:
            return {"error": f"Request error: {str(e)}"}

    def _send_request(
        self, endpoint: str, payload: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Handles sync and async requests differently."""
        if self.async_mode:
            asyncio.create_task(
                self._send_request_async(endpoint, payload)
            )  # Fire-and-forget
            return None  # No result returned in async mode
        else:
            return self._send_request_sync(
                endpoint, payload
            )  # Wait for result in sync mode

    def input(
        self,
        application_id: str,
        message: str,
        additional_parameters: Optional[Dict[str, Any]] = None,
    ):
        payload = {
            "application_id": application_id,
            "message": message,
            "additional_parameters": additional_parameters or {},
        }
        return self._send_request("/process_request/", payload)

    def output(
        self,
        application_id: str,
        message: str,
        additional_parameters: Optional[Dict[str, Any]] = None,
    ):
        payload = {
            "application_id": application_id,
            "message": message,
            "additional_parameters": additional_parameters or {},
        }
        return self._send_request("/process_response/", payload)

    def function_call(
        self,
        application_id: str,
        tool_call_id: str,
        func_name: str,
        func_args: str,
        func_result: Optional[Union[Dict, str]] = None,
        additional_parameters: Optional[Dict[str, Any]] = None,
    ):
        payload = {
            "application_id": application_id,
            "tool_call_id": tool_call_id,
            "func_name": func_name,
            "func_args": func_args,
            "func_result": func_result,
            "additional_parameters": additional_parameters or {},
        }
        return self._send_request("/process_tool_call/", payload)

    async def close(self):
        if self.async_mode:
            await self.session.aclose()
        else:
            await self.session.close()

    def __del__(self):
        if not self.async_mode:
            self.session.close()
