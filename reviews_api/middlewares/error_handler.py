from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from reviews_api.utils.exceptions import DatabaseError


async def error_handler_middleware(request: Request, call_next):
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
