from pydantic import BaseModel, Field, PositiveFloat, validator
from typing import Union
from enum import Enum
from datetime import datetime


class ReviewSentiment(Enum):
    NEGATIVE = 0
    POSITIVE = 1
    NONE = None


class RestaurantInfo(BaseModel):
    restaurant_name: str = Field(
        ..., min_length=1, description="Restaurant name or identifier"
    )
    restaurant_rating: PositiveFloat = Field(
        ..., description="Overall restaurant star rating"
    )


class ReviewInfo(BaseModel):
    review_date: str = Field(..., description="Date of published review")
    review_reviewer: str = Field(..., description="Name of reviewer")
    review_text: Union[str, None] = Field(
        ..., description="Comment/feedback about the restaurant"
    )
    review_sentiment: ReviewSentiment = Field(
        ...,
        description="Sentiment of the review: 0 (negative), 1 (positive), or None (not specified)",
    )
    review_rating: PositiveFloat = Field(..., description="Review star rating")


class RestaurantReview(BaseModel):
    restaurant: RestaurantInfo
    review: ReviewInfo


class RestaurantNameValidator:
    @validator("restaurant_name", pre=True)
    def validate_restaurant_name(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Restaurant name should contain only letters and spaces")
        return value.strip()


class RatingValidator:
    @validator("restaurant_rating", "review_rating", pre=True)
    def validate_rating(cls, value):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        return value


class ReviewerValidator:
    @validator("review_reviewer", pre=True)
    def validate_review_reviewer(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Reviewer name should contain only letters and spaces")
        return value.strip()


class ReviewDateValidator:
    @validator("review_date", pre=True)
    def validate_review_date(cls, value):
        try:
            datetime.strptime(value, "%m/%d/%Y %H:%M:%S")
        except ValueError:
            raise ValueError(
                "Invalid date format. Expected format: MM/DD/YYYY HH:MM:SS"
            )
        return value


class ReviewSentimentValidator:
    @validator("review_sentiment", pre=True)
    def validate_review_sentiment(cls, value):
        if not isinstance(value, ReviewSentiment):
            raise ValueError("Invalid sentiment value")
        return value
