from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from reviews_api.routes.routes import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
routers = [router]

for router in routers:
    app.include_router(router)
