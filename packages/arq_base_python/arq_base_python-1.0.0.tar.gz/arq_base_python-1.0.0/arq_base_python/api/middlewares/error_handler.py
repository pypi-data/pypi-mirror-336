from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
import uuid


async def http_exception_handler(request: Request, exc: HTTPException):
    response = {
        "timestamp": int(time.time() * 1000),
        "path": str(request.url.path),
        "status": exc.status_code,
        "error": "HTTP Exception",
        "message": str(exc),
        "requestId": str(uuid.uuid4())
    }
    return JSONResponse(status_code=exc.status_code, content=response)
