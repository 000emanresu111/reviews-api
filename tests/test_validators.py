import pytest

from reviews_api.models.schemas import (
    RatingValidator,
    ReviewSentimentValidator,
    ReviewSentiment,
    ReviewInfo,
    ReviewerValidator,
    DateValidator,
)


def test_validate_review_sentiment_invalid():
    invalid_review_data = {
        "review_date": "08/30/2023 12:34:56",
        "review_reviewer": "John Doe",
        "review_text": "Great food!",
        "review_sentiment": "invalid_sentiment",
        "review_rating": 4.5,
    }

    with pytest.raises(ValueError, match="Invalid sentiment value"):
        ReviewSentimentValidator.validate_review_sentiment(
            invalid_review_data["review_sentiment"]
        )


def test_validate_restaurant_rating_invalid():
    invalid_restaurant_data = {
        "restaurant_name": "Test Restaurant",
        "restaurant_rating": 6.0,  # Invalid rating value
    }

    with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
        RatingValidator.validate_rating(invalid_restaurant_data["restaurant_rating"])


def test_validate_review_rating_invalid():
    invalid_review_data = {
        "review_date": "08/30/2023 12:34:56",
        "review_reviewer": "John Doe",
        "review_text": "Great food!",
        "review_sentiment": "positive",
        "review_rating": 6.0,
    }

    with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
        RatingValidator.validate_rating(invalid_review_data["review_rating"])


def test_validate_review_reviewer_invalid():
    invalid_data = {"review_reviewer": "123 Reviewer"}
    with pytest.raises(
        ValueError, match="Reviewer name should contain only letters and spaces"
    ):
        ReviewerValidator.validate_review_reviewer(invalid_data["review_reviewer"])


def test_validate_review_date_invalid():
    invalid_data = {"review_date": "08/30/2023 12:34:56 PM"}
    with pytest.raises(
        ValueError, match="Invalid date format. Expected format: MM/DD/YYYY HH:MM:SS"
    ):
        DateValidator.validate_review_date(invalid_data["review_date"])


def test_validate_restaurant_rating_invalid():
    invalid_data = {"restaurant_rating": 6.0}
    with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
        RatingValidator.validate_rating(invalid_data["restaurant_rating"])


def test_validate_review_rating_invalid():
    invalid_data = {"review_rating": 6.0}
    with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
        RatingValidator.validate_rating(invalid_data["review_rating"])


def test_validate_review_sentiment_invalid():
    invalid_data = {"review_sentiment": "invalid_sentiment"}
    with pytest.raises(ValueError, match="Invalid sentiment value"):
        ReviewSentimentValidator.validate_review_sentiment(
            invalid_data["review_sentiment"]
        )


def test_validate_review_sentiment_valid():
    valid_data = {"review_sentiment": ReviewSentiment.POSITIVE}
    assert (
        ReviewSentimentValidator.validate_review_sentiment(
            valid_data["review_sentiment"]
        )
        == ReviewSentiment.POSITIVE
    )


def test_validate_rating_valid():
    valid_data = {"restaurant_rating": 4.5, "review_rating": 3.0}
    assert RatingValidator.validate_rating(valid_data["restaurant_rating"]) == 4.5
    assert RatingValidator.validate_rating(valid_data["review_rating"]) == 3.0


def test_validate_review_text_max_length():
    valid_data = {
        "review_date": "08/30/2023 12:34:56",
        "review_reviewer": "John Doe",
        "review_text": "A" * 501,
        "review_sentiment": ReviewSentiment.POSITIVE,
        "review_rating": 4.5,
    }

    with pytest.raises(
        ValueError, match="ensure this value has at most 500 characters"
    ):
        ReviewInfo(**valid_data)
