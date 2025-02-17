from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated, Optional, Set, List

from sqlalchemy import exc
from starlette import status

import security
from data_base.database_provider import database_provider
from data_base.database_service import DatabaseService
from data_base.sqlalchemy_db_classes import BDItem
from pydantic_classes import Item, Stats, UserNoPass

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{item_name}", response_model=Item)
async def read_item(item_name: str, database_service: Annotated[DatabaseService, Depends(database_provider)]):
    try:
        return database_service.get(item_name)
    except exc.SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {e}"
        ) from e
    except HTTPException:
        raise
@router.post("/")
async def create_item(cur_item: Item,
                      database_service: Annotated[DatabaseService, Depends(database_provider)],
                      current_user: Annotated[UserNoPass, Depends(security.get_user_and_check_active)]):
    try:
        if current_user:
            return database_service.create(cur_item)
    except exc.SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {e}"
        ) from e
    except HTTPException:
        raise

@router.put("/{item_name}")
async def update_item(item_name: str, cur_item: Item,
                      database_service: Annotated[DatabaseService, Depends(database_provider)],
                      current_user: Annotated[UserNoPass, Depends(security.get_user_and_check_active)]):
    try:
        if current_user:
            return database_service.update(item_name, cur_item)
    except exc.SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {e}"
        ) from e
    except HTTPException:
        raise

@router.get("/")
async def read_all_items(database_service: Annotated[DatabaseService, Depends(database_provider)],
                         stats: Annotated[Optional[List[str]], Query()] = None,
                         price: Optional[int] = None,
                         price_greater_than: Optional[bool] = None):
    if price and not price_greater_than:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Upon providing price, you need to also provide price_greater_than")

    validated_stats: Optional[Set[Stats]] = None

    if stats:
        validated_stats = set()

        for stat_str in stats:
            try:
                stat_enum = Stats(stat_str)
                validated_stats.add(stat_enum)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid stat: {stat_str}. Must be one of: {', '.join([s for s in Stats])}"
                )
    items = database_service.get_all(validated_stats,(price, price_greater_than))
    json = {}
    for cur_item in items:
        json[cur_item] = cur_item
    return json

@router.delete("/{item_id}")
async def delete_item(item_id: str,
                      database_service: Annotated[DatabaseService, Depends(database_provider)],
                      current_user: Annotated[UserNoPass, Depends(security.get_user_and_check_active)]):
    try:
        if current_user:
            return database_service.delete(item_id,BDItem)
    except exc.SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {e}"
        ) from e
    except HTTPException:
        raise