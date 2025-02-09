from data_base.database_service import DatabaseService
from pydantic_classes import Item

class NotFoundException(Exception):
    pass

class DatabaseServiceImplAsDict(DatabaseService):
    def __init__(self, data):
        self.data = data

    def create(self, item: Item) -> str:
        self.data[item.name] = item
        return item.name

    def get(self, name: str) -> Item:
        return self.data[name]

    def update(self, id: str, item: Item) -> bool:
        try:
            self.data[id] = item
        except KeyError:
            return False
        return True

    def delete(self, name: str) -> bool:
        try:
            del self.data[name]
        except KeyError:
            return False
        return True

    def get_all(self) -> set:
        return set(self.data.keys())


shared_data = {}

def get_db_service() -> DatabaseServiceImplAsDict:
    return DatabaseServiceImplAsDict(shared_data)