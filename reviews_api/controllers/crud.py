from reviews_api.database.database import Database


class ReviewController:
    def __init__(self, database: Database):
        self.database = database

    def add_review(self, restaurant_review):
        return self.database.add_review(restaurant_review)

    def fetch_reviews(self):
        return self.database.fetch_reviews()
