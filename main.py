from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.middlewares.error_handler import ErrorHandlerMiddleware
from app.middlewares.logger import LoggerMiddleware
from app.routes.routes import router
from fastapi.logger import logger as fastapi_logger

import logging

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app.middleware("http")(LoggerMiddleware())
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

    fastapi_logger.info("Connecting to MongoDB...")
    database = get_database()

    fastapi_logger.info("Creating collection index...")
    database.create_index([("restaurant_name", 1)])

    fastapi_logger.info("Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8086, log_config="logging_config.yaml")
