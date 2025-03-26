import httpx
import os
import uuid
from typing import Dict, Any, Optional, Union, Coroutine
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
        self,
        config: Optional[Dict[str, Any]] = None,
        async_mode: bool = True,
    ) -> None:
        load_dotenv()
        self.config = config or self._load_config_from_env()
        self.hivetrace_url = self._get_required_config("HIVETRACE_URL")
        self.hivetrace_access_token = self._get_required_config("HIVETRACE_ACCESS_TOKEN")
        self.async_mode = async_mode

        self.session = (
            httpx.AsyncClient() if async_mode 
            else httpx.Client()
        )


    async def _verify_token(self):
        url = f"{self.hivetrace_url}/api-tokens/validate"
        payload = {"token": self.hivetrace_access_token}

        try:
            if self.async_mode:
                async with httpx.AsyncClient() as client:
                    response = await client.post(url, json=payload)
            else:
                response = self.session.post(url, json=payload)
            response.raise_for_status()
        except httpx.RequestError as e:
            raise UnauthorizedError(f"Token validation failed: {e}")


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


    def _prepare_request_payload(
        self, application_id: str, message: str, additional_parameters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        application_id = self._validate_application_id(application_id)
        self._validate_message(message)
        self._validate_additional_parameters(additional_parameters)
        return {
            "application_id": application_id,
            "message": message,
            "additional_parameters": additional_parameters or {},
        }


    def _to_sync(self, coro):
        if self.async_mode:
            return coro
        
        @functools.wraps(coro)
        def wrapper(*args, **kwargs):
            return asyncio.run(coro(*args, **kwargs))
        return wrapper


    async def _send_request_async(
        self, endpoint: str, application_id: str, message: str, 
        additional_parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        payload = self._prepare_request_payload(application_id, message, additional_parameters)
        url = f"{self.hivetrace_url}/{endpoint.lstrip('/')}"
        headers = {"Authorization": f"Bearer {self.hivetrace_access_token}"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return self._handle_http_error(e)
        except httpx.RequestError as e:
            return self._handle_request_error(e, application_id)


    def _send_request_sync(
        self, endpoint: str, application_id: str, message: str, 
        additional_parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        payload = self._prepare_request_payload(application_id, message, additional_parameters)
        url = f"{self.hivetrace_url}/{endpoint.lstrip('/')}"
        headers = {"Authorization": f"Bearer {self.hivetrace_access_token}"}
        
        try:
            with httpx.Client() as client:
                response = client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return self._handle_http_error(e)
        except httpx.RequestError as e:
            return self._handle_request_error(e, application_id)


    def _send_tool_call(
        self,
        endpoint: str,
        application_id: str,
        tool_call_id: str,
        func_name: str,
        func_args: str,
        func_result: Optional[Union[Dict, str]] = None,
        additional_parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "application_id": self._validate_application_id(application_id),
            "tool_call_id": tool_call_id,
            "func_name": func_name,
            "func_args": func_args,
            "func_result": func_result,
            "additional_parameters": additional_parameters or {},
        }
        url = f"{self.hivetrace_url}/{endpoint.lstrip('/')}"
        headers = {"Authorization": f"Bearer {self.hivetrace_access_token}"}
        
        try:
            response = self.session.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return self._handle_http_error(e)
        except httpx.RequestError as e:
            return self._handle_request_error(e, application_id)


    def input(
        self, 
        application_id: str, 
        message: str, 
        additional_parameters: Optional[Dict[str, Any]] = None
    ) -> Union[Dict[str, Any], Coroutine[Any, Any, Dict[str, Any]]]:
        if self.async_mode:
            return self._send_request_async("/process_request/", application_id, message, additional_parameters)
        else:
            return self._send_request_sync("/process_request/", application_id, message, additional_parameters)


    def output(
        self, 
        application_id: str, 
        message: str, 
        additional_parameters: Optional[Dict[str, Any]] = None
    ) -> Union[Dict[str, Any], Coroutine[Any, Any, Dict[str, Any]]]:
        if self.async_mode:
            return self._send_request_async("/process_response/", application_id, message, additional_parameters)
        else:
            return self._send_request_sync("/process_response/", application_id, message, additional_parameters)


    def function_call(
        self,
        application_id: str,
        tool_call_id: str,
        func_name: str,
        func_args: str,
        func_result: Optional[Union[Dict, str]] = None,
        additional_parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return self._send_tool_call("/process_response/", application_id, tool_call_id, func_name, func_args, func_result, additional_parameters)


    async def close(self):
        if self.async_mode:
            await self.session.aclose()
        else:
            self.session.close()

    def __del__(self) -> None:
        if not self.async_mode:
            self.session.close()
