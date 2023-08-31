import pytest
from fastapi import status, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.routes.routes import router
from app.models.schemas import ErrorResponse, ScrapeReviewsResponse
from app.utils.exceptions import RestaurantNotFoundError, ReviewsNotFoundWarning

client = TestClient(router)

@patch("app.routes.routes.scrape_justeat_reviews")
def test_restaurant_not_found_error(mock_scrape_reviews):
    mock_scrape_reviews.side_effect = RestaurantNotFoundError("NonExistentRestaurant")
    
    with pytest.raises(HTTPException) as exc_info:
        client.get("/scrape-justeat-reviews?restaurant_name=NonExistentRestaurant")
    
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == ErrorResponse(success=False, error="NonExistentRestaurant").dict()

@patch("app.routes.routes.scrape_justeat_reviews")
def test_reviews_not_found_warning(mock_scrape_reviews):
    mock_scrape_reviews.side_effect = ReviewsNotFoundWarning("RestaurantWithNoReviews")
    
    with pytest.raises(HTTPException) as exc_info:
        response = client.get("/scrape-justeat-reviews?restaurant_name=RestaurantWithNoReviews")
        
        assert exc_info.value.status_code == status.HTTP_204_NO_CONTENT
        assert response.headers["X-Warning-Message"] == "There are still no reviews for this restaurant 'RestaurantWithNoReviews'"
        assert exc_info.value.detail == ErrorResponse(success=False, error="ReviewsNotFoundWarning: There are still no reviews for this restaurant 'RestaurantWithNoReviews'").dict()
