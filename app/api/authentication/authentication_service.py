from datetime import timedelta, datetime, timezone
from hashlib import sha256
from typing import Annotated, Set
from fastapi import HTTPException, Depends, Cookie, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.api.routes.users.dtos import UserViewDTO
from app.core.db_dependency import get_db
from app.core.models import User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 720


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def hash_pass(password):
    hashed_password = sha256(password.encode("utf-8")).hexdigest()
    return hashed_password


def authenticate_user(session: Session, username: str, password: str):
    new_pass = hash_pass(password)
    try:
        stmt = select(User).where(User.username == username, User.password == new_pass)
        user = session.execute(stmt).scalar_one()
        return UserViewDTO.from_query_result(user.id, user.username)
    except NoResultFound:
        return None


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def is_authenticated(session: Session, token: str):
    username, exp = decode_access_token(token)
    try:
        stmt = select(User).where(User.username == username)
        user = session.execute(stmt).scalar_one()
        return UserViewDTO.from_query_result(user.id, user.username)
    except NoResultFound:
        raise HTTPException(status_code=401, detail=str("Please log in to proceed"))


def from_token(session: Session, token: str) -> UserViewDTO | None:
    username, exp = decode_access_token(token)

    try:
        stmt = select(User).where(User.username == username)
        user = session.execute(stmt).scalar_one()
        return UserViewDTO.from_query_result(user.id, user.username)
    except NoResultFound:
        return None

def get_token_from_cookie(access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return access_token


def get_current_user(token: str = Depends(get_token_from_cookie), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        stmt = select(User).where(User.username == username)
        user = db.execute(stmt).scalar_one( )
        return UserViewDTO.from_query_result(user.id, user.username)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_user_or_raise_401(
    token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)
):
    if is_restricted(from_token(session, token), session):
        raise HTTPException(status_code=401, detail="You are currently restricted to this service")
    try:
        is_authenticated(session, token)
        return from_token(session, token)
    except HTTPException:
        raise HTTPException(status_code=401, detail=str("User doesn't exist"))
    except JWTError:
        raise HTTPException(status_code=401, detail=str("Invalid token"))



def get_token(token: str = Depends(oauth2_scheme)):
    return token

def is_restricted(user: UserViewDTO, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user.id).first()
    if user.is_restricted == 1:
        return True






