from typing import List

from app.database.db import Database
from app.models.schemas import RestaurantReview


class ReviewController:
    def __init__(self, database: Database):
        self.database = database

    def add_review(self, restaurant_review: RestaurantReview) -> None:
        return self.database.add_review(restaurant_review)

    def fetch_reviews(self) -> List[RestaurantReview]:
        return self.database.fetch_reviews()
