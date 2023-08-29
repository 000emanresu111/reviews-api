from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from reviews_api.middlewares.error_handler import error_handler_middleware
from reviews_api.routes.routes import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
)
app.add_middleware(error_handler_middleware)

app.include_router(router)
