from datetime import timedelta, timezone, datetime
from typing import Annotated

import jwt
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from starlette import status
from passlib.context import CryptContext

from data_base.database_provider import database_provider
from data_base.database_service import DatabaseService
from pydantic_classes import User, TokenData, Token
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
SECRET_KEY = config["security"]["secret_key"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/token",
    tags=["authentication"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user(token: Annotated[str, Depends(oauth2_scheme)],
                   database_service: Annotated[DatabaseService, Depends(database_provider)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = database_service.get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_user_and_check_active(current_user: Annotated[User, Depends(get_user)]) -> User:
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(input_password: str, bd_hashed_password: str):
    return pwd_context.verify(input_password, bd_hashed_password)

def authenticate_user(username: str, password: str,
                      database_service: Annotated[DatabaseService, Depends(database_provider)]):
    user = database_service.get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


@router.post("/")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(database_service=database_provider(), username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")