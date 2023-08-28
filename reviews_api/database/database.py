from datetime import datetime
from typing import List

from pymongo import MongoClient
from pymongo.collection import Collection

from reviews_api.models.schemas import ReviewInfo


class DatabaseSettings:
    DB_NAME = "restaurant_reviews"
    COLLECTION_NAME = "reviews"


class DatabaseConnection:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[DatabaseSettings.DB_NAME]
        self.collection: Collection = self.db[DatabaseSettings.COLLECTION_NAME]


class Database:
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def add_review(self, review: ReviewInfo) -> ReviewInfo:
        review_dict = review.dict()
        review_dict["review_date"] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        self.connection.collection.insert_one(review_dict)
        return review

    def fetch_reviews(self) -> List[ReviewInfo]:
        reviews = self.connection.collection.find()
        return [ReviewInfo(**review) for review in reviews]


def get_database():
    connection = DatabaseConnection()
    return Database(connection)