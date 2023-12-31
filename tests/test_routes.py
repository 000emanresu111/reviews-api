import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.controllers.crud import ReviewController
from app.database.db import get_database
from app.models.schemas import (
    RestaurantInfo,
    RestaurantReview,
    ReviewInfo,
    ReviewSentiment,
    ReviewsListResponse,
    SuccessResponse,
)
from app.routes.routes import router

client = TestClient(router)


@pytest.fixture
def mock_controller():
    return MagicMock(spec=ReviewController)


@pytest.fixture
def mock_database(request):
    database = get_database()

    def finalize():
        database.connection.collection.drop()

    request.addfinalizer(finalize)
    return database


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "OK"}


def test_add_review(mock_controller, mock_database):
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

    with patch("app.controllers.crud.ReviewController", return_value=mock_controller):
        mock_controller_instance = mock_controller.return_value
        mock_controller_instance.add_review.return_value = restaurant_review

        expected_response = SuccessResponse(
            data={
                "message": "Review added successfully",
                "restaurant_review": restaurant_review,
            }
        )

        response = client.post(
            "/reviews/add-review",
            json=restaurant_review.json(),
            content=json.dumps(restaurant_review.dict()),
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == expected_response.dict()


def test_fetch_reviews(mock_controller, mock_database):
    review_data = ReviewInfo(
        review_date="08/30/2023 12:34:56",
        review_reviewer="John Doe",
        review_text="Great beer!",
        review_sentiment="1",
        review_rating=5,
    )

    restaurant_data = RestaurantInfo(
        restaurant_name="Test Beer",
        restaurant_rating=4.2,
    )

    restaurant_review = RestaurantReview(restaurant=restaurant_data, review=review_data)
    mock_database.add_review(restaurant_review)

    with patch("app.controllers.crud.ReviewController", return_value=mock_controller):
        mock_controller_instance = mock_controller.return_value
        mock_controller_instance.fetch_reviews.return_value = [restaurant_review]

        expected_response = ReviewsListResponse(
            data=[{"restaurant": restaurant_data, "review": review_data}]
        )

        response = client.get("/reviews/fetch-reviews")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response.dict()
