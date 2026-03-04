from typing import Union
from fastapi import Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.exception_handlers import http_exception_handler as _http_exception_handler
from fastapi.exception_handlers import (
    request_validation_exception_handler as _request_validation_exception_handler,
)
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response

class LogError:
    async def request_validation_exception_handler(self, request: Request, exc: RequestValidationError) -> JSONResponse:
        error_details = []
        for error in exc.errors():
            error_detail = {
                "loc": error["loc"],
                "msg": error["msg"],
                "type": error["type"]
            }
            error_details.append(error_detail)
        
        return JSONResponse(
            status_code=400,
            content={
                "message": "Validation error",
                "result": None,
                "errors": error_details
            }
        )

    async def http_exception_handler(self, request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.detail,
                "result": None,
                "errors": None
            }
        )

    async def unhandled_exception_handler(self, request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "message": str(exc),
                "result": None,
                "errors": None
            }
        )
