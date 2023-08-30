from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.error_handler import ErrorHandlerMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.routes.routes import router

app = FastAPI()

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(ErrorHandlerMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    from app.database.db import get_database

    database = get_database()
    database.create_index([("restaurant_name", 1)])

    uvicorn.run(app, host="127.0.0.1", port=8086)
