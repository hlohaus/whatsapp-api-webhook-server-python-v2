import logging
import os
import signal
from typing import Annotated, Any, Callable, Dict, Optional, Union

import uvicorn
import uvicorn.config
from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .webhook_dto import WebhookData

class GreenAPIWebhookServer():
    def __init__(
        self,
        app: FastAPI,
        event_handler: callable,
        webhook_auth_header: str = None,
        return_keys_by_alias: bool = False,
        enable_info_logs: bool = False,
    ):
        self._event_handler = event_handler
        self._webhook_auth_header = webhook_auth_header
        self._return_keys_by_alias = return_keys_by_alias
        self._enable_info_logs = enable_info_logs
        self._init_app(app)

    def _handle_webhook(self, webhook_data: WebhookData, handler_func: callable):
        """
        Handles the incoming webhook data by calling the event handler function
        """
        parsed_data = webhook_data.model_dump(
            exclude_none=True,
            by_alias=self._return_keys_by_alias,
        )
        handler_func(webhook_data.type_webhook, parsed_data)

    def _init_app(self, app: FastAPI):
        """
        Init webhooks listener server with provided data
        """

        self._server_app = app

        @self._server_app.exception_handler(RequestValidationError)
        def validation_exception_handler(request: Request, exc: RequestValidationError):
            return JSONResponse(
                status_code=200,
                content={"message": "Incorrect data received", "errors": exc.errors()},
            )

        @self._server_app.post("/ws", status_code=status.HTTP_200_OK)
        async def webhook_endpoint(
            webhook_data: WebhookData,
            authorization: Annotated[Union[str, None], Header()] = None,
            webhook_handler_func: Callable = Depends(lambda: self._event_handler),
            webhook_auth_header: Optional[str] = Depends(
                lambda: self._webhook_auth_header
            ),
        ):
            if webhook_auth_header and authorization != f"Bearer {webhook_auth_header}":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            await self._handle_webhook(webhook_data, webhook_handler_func)

        self._server_app.state.WEBHOOK_HANDLER_FUNC = self._event_handler
        self._server_app.state.WEBHOOK_AUTH_HEADER = self._webhook_auth_header
