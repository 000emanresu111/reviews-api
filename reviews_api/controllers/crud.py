from reviews_api.database.database import Database

class ReviewController:
    def __init__(self, database: Database):
        self.database = database

    def add_review(self, review_data):
        return self.database.add_review(review_data)

    def fetch_reviews(self):
        return self.database.fetch_reviews()
