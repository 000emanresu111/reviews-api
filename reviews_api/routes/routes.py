from fastapi import APIRouter, Depends, HTTPException, Query

from reviews_api.scraper.scraping_service import scrape_justeat_reviews
from reviews_api.controllers.crud import ReviewController
from reviews_api.database.database import Database, get_database
from reviews_api.models.schemas import RestaurantReview

router = APIRouter()


def get_controller(database: Database = Depends(get_database)):
    return ReviewController(database)


@router.get("/")
async def root():
    return {"status": "OK"}


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
    try:
        return controller.fetch_reviews()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scrape-justeat-reviews")
async def scrape_justeat_reviews_endpoint(
    restaurant_name: str = Query(..., description="Name of the restaurant")
):
    try:
        reviews = scrape_justeat_reviews(restaurant_name)
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
