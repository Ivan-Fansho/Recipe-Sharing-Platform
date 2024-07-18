from pydantic import BaseModel


class UserAdminViewDTO(BaseModel):
    id: int
    username: str
    email: str
    profile_picture: str | None = None
    bio: str | None = None
    is_restricted: bool