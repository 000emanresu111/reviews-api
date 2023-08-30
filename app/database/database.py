from datetime import datetime
from typing import List
from pymongo import MongoClient
from pymongo.collection import Collection
from app.models.schemas import RestaurantReview
from bson import ObjectId


class DatabaseSettings:
    DB_NAME = "restaurant_reviews_db"
    COLLECTION_NAME = "reviews"


class DatabaseConnection:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[DatabaseSettings.DB_NAME]
        self.collection: Collection = self.db[DatabaseSettings.COLLECTION_NAME]


class Database:
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def add_review(self, review: RestaurantReview) -> RestaurantReview:
        review_dict = review.dict()
        review_dict["review_date"] = datetime.now()
        review_dict["_id"] = ObjectId()
        self.connection.collection.insert_one(review_dict)
        return review

    def fetch_reviews(self) -> List[RestaurantReview]:
        reviews = self.connection.collection.find()
        return [RestaurantReview(**review) for review in reviews]


def get_database() -> Database:
    connection = DatabaseConnection()
    return Database(connection)
