from abc import ABC, abstractmethod
from typing import Optional, Set

from pydantic_classes import Item

class DatabaseService(ABC):

    @abstractmethod
    def create(self, item: Item) -> str: pass

    @abstractmethod
    def get(self, id: str) -> Item: pass

    @abstractmethod
    def update(self, id: str, item: Item) -> bool: pass

    @abstractmethod
    def delete(self, id: str) -> bool: pass

    @abstractmethod
    def get_all(self, stats: Optional[Set[str]] = None, price: Optional[tuple[int, bool]] = None) -> set: pass
