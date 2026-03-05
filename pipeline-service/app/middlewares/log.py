from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.utils.log import logger
import json

class LogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.logger = logger
        
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        
        # Capture response body
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        
        # Reconstruct response since body_iterator was consumed
        response = Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )

        endpoint = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
        user_id = request.state.user.get("user_id") if hasattr(request.state, "user") else None
        
        try:
            resp_json = json.loads(response_body.decode("utf-8"))
        except:
            resp_json = response_body.decode("utf-8") if response_body else None

        log_level = "INFO" if response.status_code < 400 else "ERROR"
        message = "Success" if response.status_code < 400 else "Fail"

        self.logger.bind(
            method=request.method, 
            url=endpoint, 
            status_code=response.status_code,
            response_body=resp_json,
            user_id=user_id
        ).log(log_level, message)
        
        return response
