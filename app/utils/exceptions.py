from fastapi import HTTPException


class DatabaseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class RestaurantNotFoundError(HTTPException):
    def __init__(self, restaurant_name: str):
        detail = f"Restaurant '{restaurant_name}' not found"
        super().__init__(status_code=404, detail=detail)
