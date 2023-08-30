from fastapi import APIRouter, Depends, HTTPException

from app.controllers.crud import ReviewController
from app.database.db import Database, get_database
from app.models.schemas import RestaurantNameQuery, RestaurantReview
from app.scraper.scraping_service import scrape_justeat_reviews
from app.utils.exceptions import RestaurantNotFoundError

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
    query_params: RestaurantNameQuery
):
    try:
        reviews = scrape_justeat_reviews(query_params.restaurant_name)
        if not reviews:
            raise HTTPException(status_code=404, detail="No reviews found for the restaurant")
        return reviews
    except RestaurantNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
