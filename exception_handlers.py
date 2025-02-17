from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging
from starlette import status
from pydantic import ValidationError

def register_exception_handlers(app: FastAPI):
    """Registers custom exception handlers with the FastAPI application."""

    @app.exception_handler(SQLAlchemyError)
    async def sql_alchemy_error_exception_handler(request: Request, exc: SQLAlchemyError):
        logging.exception(f"Database error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "A database error occurred. Please try again later."},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logging.warning(f"HTTPException: {exc.detail} (status code: {exc.status_code})")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        logging.warning(f"Validation Error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,  # Use 400 Bad Request
            content={"detail": f"Validation error occurred: {exc}"},  # User-friendly message
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logging.exception(f"An unexpected error occurred: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred. Please contact support."},
        )

    return app