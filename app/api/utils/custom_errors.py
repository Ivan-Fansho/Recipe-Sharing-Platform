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

class UserNotFoundException(CustomHTTPException):
    def __init__(self, detail: str = "User you are trying to access was not found"):
        super().__init__(status_code=404, detail=detail)

class CommentNotFoundException(CustomHTTPException):
    def __init__(self, detail: str = "Comment you are trying to access was not found"):
        super().__init__(status_code=404, detail=detail)

class RatingAlreadyExistsException(CustomHTTPException):
    def __init__(self, detail: str = "you have already given a rating to this recipe"):
        super().__init__(status_code=400, detail=detail)

class WrongSortInputException(CustomHTTPException):
    def __init__(self, detail: str = "you can only choose one of the available sorts: 'asc', 'desc'"):
        super().__init__(status_code=400, detail=detail)

class FavoriteAlreadyExistsException(CustomHTTPException):
    def __init__(self, detail: str = "you have already have this recipe in your favorites list"):
        super().__init__(status_code=400, detail=detail)

class FavoriteDoesntExistsException(CustomHTTPException):
    def __init__(self, detail: str = "you have dont have this recipe in your favorites"):
        super().__init__(status_code=404, detail=detail)

class BlockedUserException(CustomHTTPException):
    def __init__(self, detail: str = "You dont have access to this function"):
        super().__init__(status_code=403, detail=detail)

class NotAdminUserException(CustomHTTPException):
    def __init__(self, detail: str = "This is Admin only function"):
        super().__init__(status_code=403, detail=detail)

class InvalidRestrictionInputException(CustomHTTPException):
    def __init__(self, detail: str = "You can only input 'Yes' or 'No'"):
        super().__init__(status_code=400, detail=detail)

class UserAlreadyBlockedException(CustomHTTPException):
    def __init__(self, detail: str = "you have already blocked this user"):
        super().__init__(status_code=400, detail=detail)

class UserAlreadyUnblockedException(CustomHTTPException):
    def __init__(self, detail: str = "User is already unblocked"):
        super().__init__(status_code=400, detail=detail)

class InvalidRestrictionInputExceptionv2(CustomHTTPException):
    def __init__(self, detail: str = "You can only input 'block' or 'unblock'"):
        super().__init__(status_code=400, detail=detail)

class ProfanityFoundException(CustomHTTPException):
    def __init__(self, detail: str = "You cannot post any profanity"):
        super().__init__(status_code=400, detail=detail)