from enum import Enum
from pydantic import BaseModel, Field


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
    sell_price: float = Field(..., lt=price)