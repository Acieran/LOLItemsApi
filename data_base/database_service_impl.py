import sqlite3
from data_base.database_service import DatabaseService
from pydantic_classes import Item


class DatabaseServiceImpl(DatabaseService):

    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

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

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute("CREATE TABLE movie(title, year, score)")