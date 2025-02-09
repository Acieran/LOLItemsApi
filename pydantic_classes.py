from enum import Enum
from pydantic import BaseModel

class Stats(str, Enum):
    armor = "Armor"
    health = "Health"
    health_regen = "Health Regen"
    magic_resist = "Magic Resist"
    omni_vamp = "Omni Vamp"

class Item(BaseModel):
    name: str
    stats: dict[Stats, int]
    description: str | None = None
    price: float
    sell_price: float