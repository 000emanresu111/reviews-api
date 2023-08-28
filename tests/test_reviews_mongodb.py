from fastapi.testclient import TestClient
from reviews_api.routes.routes import router
from reviews_api.controllers.crud import ReviewController
from reviews_api.models.schemas import RestaurantReview, ReviewInfo, RestaurantInfo, ReviewSentiment
from unittest.mock import patch, MagicMock
from reviews_api.database.database import Database
import pytest
import json
from enum import Enum

client = TestClient(router)

class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)
    
@pytest.fixture
def mock_controller():
    return MagicMock(spec=ReviewController)

def test_add_review(mock_controller):
    review_data = ReviewInfo(
        review_date="08/30/2023 12:34:56",
        review_reviewer="John Doe",
        review_text="Great food!",
        review_sentiment=ReviewSentiment.POSITIVE.value,
        review_rating=4.5,
    )

    restaurant_data = RestaurantInfo(
        restaurant_name="Test Restaurant",
        restaurant_rating=4.5,
    )

    restaurant_review = RestaurantReview(restaurant=restaurant_data, review=review_data)
    print(restaurant_review.json())


    with patch("reviews_api.controllers.crud.ReviewController", return_value=mock_controller):
        mock_controller_instance = mock_controller.return_value
        mock_controller_instance.add_review.return_value = restaurant_review

        response = client.post(
            "/reviews/add-review",
            json=restaurant_review.json(),
            content=json.dumps(restaurant_review.dict()),
            headers={"Content-Type": "application/json"},
        )

        print("response", response.json())

        assert response.status_code == 200
        assert response.json() == restaurant_review.dict()