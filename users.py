from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from sqlalchemy import exc
from starlette import status

from security import get_user_and_check_active,hash_password
from data_base.database_provider import database_provider
from data_base.database_service import DatabaseService
from data_base.sqlalchemy_db_classes import BDUser
from pydantic_classes import User, UserNoPass

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/me")
async def read_users_me(current_user: Annotated[UserNoPass, Depends(get_user_and_check_active)]):
    return current_user

@router.get("/{user_name}", response_model=User, response_model_exclude={'password'})
async def get_user(user_name: str,
                    database_service: Annotated[DatabaseService, Depends(database_provider)],
                    current_user: Annotated[UserNoPass, Depends(get_user_and_check_active)]):
    try:
        if current_user:
            return database_service.get_user(user_name)
    except exc.SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {e}"
        ) from e
    except HTTPException:
        raise

@router.post("/")
async def create_user(user: User,
                      database_service: Annotated[DatabaseService, Depends(database_provider)],
                      current_user: Annotated[UserNoPass, Depends(get_user_and_check_active)]):
    try:
        if current_user:
            user.password = hash_password(user.password)
            return database_service.create_user(user)
    except exc.SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {e}"
        ) from e
    except HTTPException:
        raise

@router.put("/{user_name}")
async def update_user(user_name: str, user: User,
                      database_service: Annotated[DatabaseService, Depends(database_provider)],
                      current_user: Annotated[UserNoPass, Depends(get_user_and_check_active)]):
    try:
        if current_user:
            if user.password:
                user.password = hash_password(user.password)
            return database_service.update_user(user_name, user)
    except exc.SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {e}"
        ) from e
    except HTTPException:
        raise

@router.put("/deactivate/{user_name}")
async def deactivate_user(user_name: str,
                          database_service: Annotated[DatabaseService, Depends(database_provider)],
                          current_user: Annotated[UserNoPass, Depends(get_user_and_check_active)]):
    try:
        if current_user:
            user = database_service.get_user(user_name)
            user.active = False
            return database_service.update_user(user_name, user)
    except exc.SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {e}"
        ) from e
    except HTTPException:
        raise


@router.delete("/{user_name}")
async def delete_user(user_name: str,
                      database_service: Annotated[DatabaseService, Depends(database_provider)],
                      current_user: Annotated[UserNoPass, Depends(get_user_and_check_active)]):
    try:
        if current_user:
            return database_service.delete(user_name, BDUser)
    except exc.SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {e}"
        ) from e
    except HTTPException:
        raise