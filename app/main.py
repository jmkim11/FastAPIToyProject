from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.posts import router as posts_router
from app.web.pages import router as pages_router

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


from app.core.errors import AppError
from app.core.exception_handlers import (
    app_error_handler,
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)

app = FastAPI(title="Mini MVC with FastAPI")

# 정적 파일(CSS/JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 웹 페이지(HTML)
app.include_router(pages_router)

# JSON API
app.include_router(posts_router)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)