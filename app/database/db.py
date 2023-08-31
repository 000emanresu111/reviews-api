import os
from datetime import datetime
from typing import List

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection

from app.models.schemas import RestaurantReview

load_dotenv()


class DatabaseSettings:
    MONGODB_URI = os.getenv("MONGODB_URI_LOCAL")
    MONGODB_NAME = os.getenv("MONGODB_NAME")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")


class DatabaseConnection:
    def __init__(self):
        self.client = MongoClient(DatabaseSettings.MONGODB_URI)
        self.db = self.client[DatabaseSettings.MONGODB_NAME]
        self.collection: Collection = self.db[DatabaseSettings.COLLECTION_NAME]


class Database:
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def create_index(self, keys: list, unique: bool = False):
        self.connection.collection.create_index(keys, unique=unique)

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
