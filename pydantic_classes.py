from enum import Enum
from fastapi import HTTPException
from typing import Annotated

from pydantic import BaseModel, Field, AfterValidator, field_validator
from starlette import status


@field_validator('sell_price')
def validate_sell_price(cls, value, values):
    """Validates that the sell_price is less than the price."""
    price = values.get('price')
    if price is not None and value >= price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="sell_price must be less than price")
    return value

class Stats(str, Enum):
    armor = "Armor"
    health = "Health"
    health_regen = "Health Regen"
    magic_resist = "Magic Resist"
    omni_vamp = "Omni Vamp"

class Item(BaseModel):
    name: str = Field(...,max_length=30)
    stats: dict[Stats, Annotated[int]]
    description: str | None = Field(None, max_length=1000)
    price: float = Field(..., ge=0)
    sell_price: float