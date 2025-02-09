from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from pydantic_classes import Item
from data_base.database_service_impl_as_dict import get_db_service,DatabaseServiceImplAsDict

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: str, database_service: Annotated[DatabaseServiceImplAsDict, Depends(get_db_service)]):
    try:
        return database_service.get(item_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")

@router.post("/")
async def create_item(cur_item: Item, database_service: Annotated[
    DatabaseServiceImplAsDict, Depends(get_db_service)]):
    return database_service.create(cur_item)

@router.put("/{item_id}")
async def update_item(item_id: str, cur_item: Item, database_service: Annotated[
    DatabaseServiceImplAsDict, Depends(get_db_service)]):
    return database_service.update(item_id, cur_item)

@router.get("/")
async def read_all_items(database_service: Annotated[DatabaseServiceImplAsDict, Depends(get_db_service)]):
    items = database_service.get_all()
    json = {}
    for cur_item in items:
        json[cur_item] = cur_item
    return json

@router.delete("/{item_id}")
async def delete_item(item_id: str, database_service: Annotated[DatabaseServiceImplAsDict, Depends(get_db_service)]):
    return database_service.delete(item_id)