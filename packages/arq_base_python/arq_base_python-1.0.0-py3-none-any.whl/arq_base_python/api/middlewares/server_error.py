import uuid
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse


class InternalServerErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            return await self.internal_server_error_handler(request, exc)

    async def internal_server_error_handler(self, request: Request, exc: Exception):
        response = {
            "timestamp": int(time.time() * 1000),
            "path": str(request.url.path),
            "status": 500,
            "error": "Internal Server Error",
            "message": str(exc),
            "requestId": str(uuid.uuid4())
        }
        return JSONResponse(status_code=500, content=response)


async def internal_server_error_handler(request: Request, exc: Exception):
    response = {
        "timestamp": int(time.time() * 1000),
        "path": str(request.url.path),
        "status": 500,
        "error": "Internal Server Error",
        "message": str(exc),
        "requestId": str(uuid.uuid4())
    }
    return JSONResponse(status_code=500, content=response)
