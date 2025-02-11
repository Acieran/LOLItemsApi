from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated, Optional, Set, List

from sqlalchemy import exc
from starlette.requests import Request
from starlette.responses import JSONResponse

from data_base.database_provider import database_provider
from data_base.database_service import DatabaseService
from pydantic_classes import Item

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{item_name}", response_model=Item)
async def read_item(item_name: str, database_service: Annotated[DatabaseService, Depends(database_provider)]):
    try:
        return database_service.get(item_name)
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")

@router.post("/")
async def create_item(cur_item: Item, database_service: Annotated[DatabaseService, Depends(database_provider)]):
    return database_service.create(cur_item)

@router.put("/{item_id}")
async def update_item(item_id: str, cur_item: Item, database_service: Annotated[DatabaseService, Depends(database_provider)]):
    return database_service.update(item_id, cur_item)

@router.get("/")
async def read_all_items(database_service: Annotated[DatabaseService, Depends(database_provider)],
                         stats: Annotated[Optional[List[str]], Query()] = None,
                         price: Optional[int] = None,
                         price_greater_than: Optional[bool] = None):
    try:
        stats_set: Optional[Set[str]] = set(stats) if stats else None
        items = database_service.get_all(stats_set,(price, price_greater_than))
        json = {}
        for cur_item in items:
            json[cur_item] = cur_item
        return json
    except exc.SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=e)

@router.delete("/{item_id}")
async def delete_item(item_id: str, database_service: Annotated[DatabaseService, Depends(database_provider)]):
    return database_service.delete(item_id)