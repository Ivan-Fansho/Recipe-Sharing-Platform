from pydantic import BaseModel, field_validator

from app.api.utils.validation_errors import RatingValidationError


class GiveRatingDTO(BaseModel):
    recipe_id: int
    rating: int

    @field_validator('rating')
    def validate_rating(cls, r):
        if r < 1 or r > 5:
            raise RatingValidationError('Rating must be between 1 and 5')
        return r