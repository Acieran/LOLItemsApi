from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from data_base.database_provider import database_provider, DatabaseProvider, get_dict_db_service, get_sql_db_service
from data_base.database_service import DatabaseService
from pydantic_classes import Item
from data_base.database_service_impl_as_dict import get_db_service,DatabaseServiceImplAsDict

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
async def read_all_items(database_service: Annotated[DatabaseService, Depends(database_provider)]):
    items = database_service.get_all()
    json = {}
    for cur_item in items:
        json[cur_item] = cur_item
    return json

@router.delete("/{item_id}")
async def delete_item(item_id: str, database_service: Annotated[DatabaseService, Depends(database_provider)]):
    return database_service.delete(item_id)