from data_base.database_service import DatabaseService
from pydantic_classes import Item
from data_base.sqlalchemy_db import BDItem, BDStat, Base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select


class DatabaseServiceImpl(DatabaseService):

    def __init__(self):
        self.engine = create_engine("sqlite:///database.db", echo=True)
        Base.metadata.create_all(self.engine)

    def create(self, item: Item) -> str:
        with Session(self.engine) as session:
            db_item = BDItem(
                name=item.name,
                description=item.description,
                price=item.price,
                sell_price=item.sell_price
            )
            for stat_name, stat_value in item.stats.items():
                db_item.stats.append(BDStat(name=stat_name , value=stat_value))
            session.add(db_item)
            session.commit()
        return item.name

    def get(self, name: str) -> Item:
        session = Session(self.engine)

        stmt = (
            select(BDItem)
            .join(BDStat.item)
            .where(BDItem.name == name)
        )
        item = session.scalars(stmt)
        return item

    def update(self, id: str, item: Item) -> bool:
        pass

    def delete(self, name: str) -> bool:
        pass

    def get_all(self) -> set:
        pass