from fastapi import APIRouter, Depends, HTTPException

from reviews_api.controllers.crud import ReviewController
from reviews_api.database.database import Database, get_database
from reviews_api.models.schemas import RestaurantReview

router = APIRouter()


def get_controller(database: Database = Depends(get_database)):
    return ReviewController(database)


@router.get("/")
async def root():
    return {"message": "Ciao!"}


@router.post("/reviews/add-review")
async def add_review(
    review: RestaurantReview, controller: ReviewController = Depends(get_controller)
):
    try:
        return controller.add_review(review)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reviews/fetch-reviews")
async def fetch_reviews(controller: ReviewController = Depends(get_controller)):
    return controller.fetch_reviews()
