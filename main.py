from fastapi import FastAPI, Depends
from reviews_api.models.schemas import RestaurantReview
from reviews_api.controllers.crud import ReviewController
from reviews_api.database.database import Database, get_database
from reviews_api.routes.routes import router
from fastapi.middleware.cors import CORSMiddleware


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
