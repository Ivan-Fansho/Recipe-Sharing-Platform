import re
from pydantic import BaseModel, field_validator

from app.api.utils.validation_errors import UsernameValidationError, PasswordValidationError, \
    EmailValidationError


class UserDTO(BaseModel):
    username: str
    password: str
    email: str

    @field_validator("username")
    def validate_username(cls, v):
        if not re.match(r"^\w{2,20}$", v):
            raise UsernameValidationError("Username must be between 2 and 20 characters and contain only alphanumeric characters and underscores.")
        return v
    @field_validator("password")
    def validate_password(cls, p):
        if len(p) < 8 or len(p) > 20:
            raise PasswordValidationError("Password must be between 8 and 20 characters long.")
        if not any(char.isupper() for char in p):
            raise PasswordValidationError("Password must contain at least one uppercase letter")
        if not any(char.isdigit() for char in p):
            raise PasswordValidationError("Password must contain at least one digit")
        if not any(char in "!@#$%^&*()_+{}[]:;<>,.?~\\-" for char in p):
            raise PasswordValidationError("Password must contain at least one special character")
        return p

    @field_validator("email")
    def validate_email(cls, e):
        if not re.match(r"^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$", e):
            raise EmailValidationError("Pleas input a valid email address")
        return e




class UserViewDTO(BaseModel):
    id: int
    username: str

    @classmethod
    def from_query_result(cls, id, username):
        return cls(id=id, username=username)

class UpdateUserDTO(BaseModel):
    email: str | None = None
    password: str | None = None
    photo: str | None = None
    bio: str | None = None


    @field_validator('password')
    def validate_password(cls, p):
        if len(p) < 8:
            raise PasswordValidationError('Password must be at least 8 characters long')
        if not any(char.isupper() for char in p):
            raise PasswordValidationError('Password must contain at least one uppercase letter')
        if not any(char.isdigit() for char in p):
            raise PasswordValidationError('Password must contain at least one digit')
        if not any(char in '!@#$%^&*()_+{}[]:;<>,.?~\\-' for char in p):
            raise PasswordValidationError('Password must contain at least one special character')
        return p

    @field_validator('email')
    def validate_email(cls, e):
        if not re.match(r"^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$", e):
            raise EmailValidationError('Pleas input a valid email address')
        return e




class ShowUserDTO(BaseModel):
    id: int
    username: str
    email: str
    bio: str | None = None
    profile_pic: str | None = None
