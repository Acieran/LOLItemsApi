from typing import Optional, Set, Type

from fastapi import HTTPException
from starlette import status

from data_base.database_service import DatabaseService
from pydantic_classes import Item, User, UserNoPass
from data_base.sqlalchemy_db_classes import BDItem, BDStat, Base, BDUser
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy import create_engine, select, exc, and_


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

    def get(self, item_id: str) -> Item:
        try:
            with Session(self.engine) as session:
                stmt = (
                    select(BDItem,BDStat)
                    .join(BDStat, BDStat.item_name == BDItem.name)
                    .where(BDItem.name == item_id)
                )
                db_item = session.scalars(stmt).first()
                if not db_item:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
                item = Item(name=db_item.name, description=db_item.description,
                            price=db_item.price, sell_price=db_item.sell_price, stats={})
                for db_stat in db_item.stats:
                    item.stats[db_stat.name] = db_stat.value
            return item
        except exc.SQLAlchemyError as e:
            raise e

    def update(self, item_id: str, item: Item) -> Item:
        try:
            with Session(self.engine) as session:
                stmt = (
                    select(BDItem,BDStat)
                    .join(BDStat, BDStat.item_name == BDItem.name)
                    .where(BDItem.name == item_id)
                )
                db_item = session.scalars(stmt).first()
                if not db_item:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
                for attr in ['name', 'description', 'price', 'sell_price']:
                    setattr(db_item, attr, getattr(item, attr))
                db_item.stats = []
                item = Item(name=db_item.name, description=db_item.description,
                            price=db_item.price, sell_price=db_item.sell_price, stats={})
                for stat_name, stat_value in item.stats.items():
                    db_item.stats.append(BDStat(name=stat_name, value=stat_value))
                    item.stats[stat_name] = stat_value
                session.commit()
            return item
        except exc.SQLAlchemyError as e:
            raise e

    def delete(self, item_id: str, cls: Type[DeclarativeBase]) -> bool:
        try:
            with Session(self.engine) as session:
                db_item = session.get(cls, item_id)
                if not db_item:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
                session.delete(db_item)
                session.commit()
            return True
        except exc.SQLAlchemyError as e:
            raise e

    def get_all(self, stats: Optional[Set[str]] = None, price: Optional[tuple[int, bool]] = None) -> set:
        try:
            with (Session(self.engine) as session):
                stmt = select(BDItem.name)
                if price[0] is not None:
                    if price[1]:
                        stmt = stmt.where(BDItem.price >= price[0])
                    else:
                        stmt = stmt.where(BDItem.price < price[0])

                if stats is not None and len(stats) > 0:
                    stat_conditions = [BDItem.name.in_(select(BDStat.item_name).where(BDStat.name == stat)) for stat in
                                       stats]
                    stmt = stmt.where(and_(*stat_conditions))

                bd_items = session.execute(stmt).all()
                if not bd_items:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
                items_set = set()
                for item in bd_items:
                    items_set.add(item.name)
                return items_set
        except exc.SQLAlchemyError as e:
            raise e

    def get_user(self, username: str) -> User:
        try:
            with Session(self.engine) as session:
                stmt = (
                    select(BDUser)
                    .where(BDUser.user_name == username)
                )
                db_item = session.scalars(stmt).first()
                if not db_item:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with name - {username} not found")
                user = User(user_name=db_item.user_name, password=db_item.password, active=db_item.active)
            return user
        except exc.SQLAlchemyError as e:
            raise e

    def create_user(self, user: User) -> str:
        try:
            with Session(self.engine) as session:
                session.expire_on_commit = False
                bd_user = BDUser(
                    user_name=user.user_name,
                    password=user.password,
                    active=True
                )
                session.add(bd_user)
                session.commit()
            return bd_user.user_name
        except exc.SQLAlchemyError as e:
            raise e

    def update_user(self, username: str, user: User | UserNoPass) -> User:
        try:
            with Session(self.engine) as session:
                stmt = (
                    select(BDUser)
                    .where(BDUser.user_name == username)
                )
                db_item = session.scalars(stmt).first()
                if not db_item:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
                if user.password:
                    db_item.password = user.password
                for attr in ['user_name', 'active']:
                    setattr(db_item, attr, getattr(user, attr))
                session.commit()
                user = User(user_name=db_item.user_name, password=db_item.password, active=db_item.active)
            return user
        except exc.SQLAlchemyError as e:
            raise e