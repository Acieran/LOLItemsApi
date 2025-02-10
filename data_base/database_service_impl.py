from data_base.database_service import DatabaseService
from pydantic_classes import Item
from data_base.sqlalchemy_db import BDItem, BDStat, Base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, exc


class DatabaseServiceImpl(DatabaseService):

    def __init__(self):
        self.engine = create_engine("sqlite:///data_base/database.db", echo=True)
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
        with Session(self.engine) as session:
            stmt = (
                select(BDItem,BDStat)
                .join(BDStat, BDStat.item_name == BDItem.name)
                .where(BDItem.name == name)
            )
            db_item = session.scalars(stmt).first()
            item = Item(name=db_item.name, description=db_item.description,
                        price=db_item.price, sell_price=db_item.sell_price, stats={})
            for db_stat in db_item.stats:
                item.stats[db_stat.name] = db_stat.value
        return item

    def update(self, name: str, item: Item) -> bool:
        try:
            with Session(self.engine) as session:
                stmt = (
                    select(BDItem,BDStat)
                    .join(BDStat, BDStat.item_name == BDItem.name)
                    .where(BDItem.name == name)
                )
                db_item = session.scalars(stmt).first()
                for attr in ['name', 'description', 'price', 'sell_price']:
                    setattr(db_item, attr, getattr(item, attr))
                db_item.stats = []
                for stat_name, stat_value in item.stats.items():
                    db_item.stats.append(BDStat(name=stat_name, value=stat_value))
                session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def delete(self, name: str) -> bool:
        try:
            with Session(self.engine) as session:
                bd_item = session.get(BDItem, name)
                session.delete(bd_item)
                session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    def get_all(self) -> set:
        try:
            with Session(self.engine) as session:
                stmt = select(BDItem.name)
                bd_items = session.execute(stmt).all()
                items_set = set()
                for bd_item in bd_items:
                    items_set.add(bd_item.name)
                return items_set
        except exc.SQLAlchemyError as e:
            raise e
