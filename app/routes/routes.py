from fastapi import APIRouter, Depends, HTTPException, status

from app.controllers.crud import ReviewController
from app.database.db import Database, get_database
from app.models.schemas import (
    ErrorResponse,
    RestaurantReview,
    ReviewsListResponse,
    ScrapeReviewsResponse,
    SuccessResponse,
)
from app.scraper.scraping_service import scrape_justeat_reviews
from app.utils.exceptions import RestaurantNotFoundError, ReviewsNotFoundWarning

router = APIRouter()


def get_controller(database: Database = Depends(get_database)):
    return ReviewController(database)


@router.get("/", summary="Health Check", description="Check the API health status.")
async def root():
    return {"status": "OK"}


@router.post(
    "/reviews/add-review",
    response_model=SuccessResponse,
    status_code=201,
    summary="Add a Review",
    description="Add a new review for a restaurant.",
)
async def add_review(
    review: RestaurantReview, controller: ReviewController = Depends(get_controller)
):
    try:
        controller.add_review(review)
        response_data = {
            "message": "Review added successfully",
            "restaurant_review": review,
        }
        return SuccessResponse(data=response_data)
    except Exception as e:
        error_response = ErrorResponse(error=str(e)).dict()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_response
        )


@router.get(
    "/reviews/fetch-reviews",
    response_model=ReviewsListResponse,
    status_code=200,
    summary="Fetch Reviews",
    description="Fetch a list of all restaurant reviews.",
)
async def fetch_reviews(controller: ReviewController = Depends(get_controller)):
    try:
        reviews = controller.fetch_reviews()
        return ReviewsListResponse(data=reviews)
    except Exception as e:
        error_response = ErrorResponse(error=str(e)).dict()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_response
        )


@router.get(
    "/scrape-justeat-reviews",
    response_model=ScrapeReviewsResponse,
    status_code=200,
    summary="Scrape JustEat Reviews",
    description="Scrape reviews for a restaurant from JustEat.",
)
async def scrape_justeat_reviews_endpoint(restaurant_name: str):
    try:
        scraped_reviews = scrape_justeat_reviews(restaurant_name)
        return ScrapeReviewsResponse(
            reviews=scraped_reviews, message="Reviews scraped successfully"
        )
    except ReviewsNotFoundWarning as e:
        response_headers = {"X-Warning-Message": str(e)}
        error_response = ErrorResponse(error=str(e)).dict()
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            headers=response_headers,
            detail=error_response,
        )
    except RestaurantNotFoundError as e:
        error_response = ErrorResponse(error=str(e)).dict()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=error_response
        )
    except Exception as e:
        error_response = ErrorResponse(error=str(e)).dict()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_response
        )
