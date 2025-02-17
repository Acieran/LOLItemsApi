from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, field_validator

class SellPriceValidationError(ValueError):  # Inherit from ValueError or Exception
    """Custom exception for sell_price validation errors."""
    pass

class Stats(str, Enum):
    armor = "Armor"
    health = "Health"
    health_regen = "Health Regen"
    magic_resist = "Magic Resist"
    omni_vamp = "Omni Vamp"

class Item(BaseModel):
    name: str = Field(...,max_length=30)
    stats: dict[Stats, int]
    description: str | None = Field(None, max_length=1000)
    price: float = Field(..., ge=0)
    sell_price: float

    @field_validator('sell_price')
    def validate_sell_price(cls, value, values):
        """Validates that the sell_price is less than the price."""
        price = values.get('price')
        if price is not None and value >= price:
            raise SellPriceValidationError("sell_price must be less than price") # New exception
        return value

class UserNoPass(BaseModel):
    user_name: str = Field(..., max_length=30)
    active: bool = Field(default=True)

class User(UserNoPass):
    password: str = Field(..., min_length=6)


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None