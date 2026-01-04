from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.errors import AppError

def error_response(status_code: int, code: str, message: str, details: dict | None = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "ok": False,
            "error": {
                "code": code,
                "message": message,
                "details": details or {},
            },
        },
    )

async def app_error_handler(request: Request, exc: AppError):
    return error_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        details=exc.details or {},
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # FastAPI/Starlette 기본 HTTPException도 포맷 통일
    return error_response(
        status_code=exc.status_code,
        code="HTTP_EXCEPTION",
        message=str(exc.detail),
        details={},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Pydantic 검증 에러 포맷 통일
    return error_response(
        status_code=422,
        code="VALIDATION_ERROR",
        message="Request validation failed",
        details={"errors": exc.errors()},
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    # 예상 못한 에러(500)도 통일
    return error_response(
        status_code=500,
        code="INTERNAL_SERVER_ERROR",
        message="Unexpected server error",
        details={},
    )