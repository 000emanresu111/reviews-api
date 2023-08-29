from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from reviews_api.utils.exceptions import DatabaseError
from starlette.middleware.base import BaseHTTPMiddleware

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except DatabaseError as e:
            return JSONResponse(
                status_code=500,
                content={"message": str(e)},
            )
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"message": e.detail},
            )
        except ValidationError as e:
            errors = e.errors()
            error_messages = []
            for error in errors:
                error_messages.append({"field": error["loc"][2], "message": error["msg"]})
            return JSONResponse(
                status_code=422,
                content={"message": "Validation error", "errors": error_messages},
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"message": "An internal server error occurred."},
            )
