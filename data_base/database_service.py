from abc import ABC, abstractmethod
from typing import Optional, Set, Type

from sqlalchemy.orm import DeclarativeBase

from pydantic_classes import Item, User, UserNoPass


class DatabaseService(ABC):

    @abstractmethod
    def create(self, item: Item) -> str: pass

    @abstractmethod
    def get(self, name: str) -> Item: pass

    @abstractmethod
    def update(self, name: str, item: Item) -> bool: pass

    @abstractmethod
    def delete(self, name: str, cls: Type[DeclarativeBase]) -> bool: pass

    @abstractmethod
    def get_all(self, stats: Optional[Set[str]] = None, price: Optional[tuple[int, bool]] = None) -> set: pass

    @abstractmethod
    def get_user(self, username: str) -> User: pass

    @abstractmethod
    def create_user(self, user: User) -> str: pass

    @abstractmethod
    def update_user(self, username: str, user: User | UserNoPass) -> bool: pass