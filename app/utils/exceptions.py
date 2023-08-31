from fastapi import HTTPException


class DatabaseError(HTTPException):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class RestaurantNotFoundError(HTTPException):
    def __init__(self, restaurant_name: str):
        self.message = f"Restaurant '{restaurant_name}' not found"


class ReviewsNotFoundWarning(HTTPException):
    def __init__(self, restaurant_name: str):
        self.message = (
            f"There are still no reviews for this restaurant '{restaurant_name}'"
        )
