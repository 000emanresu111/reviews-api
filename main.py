from fastapi import FastAPI, Depends
from reviews_api.models.schemas import RestaurantReview
from reviews_api.controllers.crud import ReviewController
from reviews_api.database.database import Database, get_database
from reviews_api.routes import router

app = FastAPI()

app.include_router(router, prefix="/reviews")
