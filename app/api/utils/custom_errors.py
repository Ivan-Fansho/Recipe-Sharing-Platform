from fastapi import HTTPException

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class WrongUserException(CustomHTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=401, detail=detail)


class WrongCategoryException(CustomHTTPException):
    def __init__(self, detail: str ="Category not supported please choose one of the available categories:"
            " [Pizzas, Soups, Deserts, Breakfast, Main Course, Appetizers, Beverages, Salads, Sandwiches]"):
        super( ).__init__(status_code=400, detail=detail)

class RecipeNotFoundException(CustomHTTPException):
    def __init__(self, detail: str = "Recipe you are trying to access was not found"):
        super().__init__(status_code=404, detail=detail)

class CommentNotFoundException(CustomHTTPException):
    def __init__(self, detail: str = "Comment you are trying to access was not found"):
        super().__init__(status_code=404, detail=detail)

class RatingAlreadyExistsException(CustomHTTPException):
    def __init__(self, detail: str = "you have already given a rating to this recipe"):
        super().__init__(status_code=400, detail=detail)
