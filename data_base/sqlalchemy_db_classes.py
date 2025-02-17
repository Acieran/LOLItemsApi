from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class BDItem(Base):
    __tablename__ = "items"
    name: Mapped[str] = mapped_column(String(30),primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(String(1000),nullable=True)
    price: Mapped[Optional[float]]
    sell_price: Mapped[Optional[float]]
    stats: Mapped[List["BDStat"]] = relationship(
        back_populates="item", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"Item(Name={self.name!r}, Description={self.description!r}, Price={self.price!r}, Sell price={self.sell_price!r})"

class BDStat(Base):
    __tablename__ = "stats"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[int]
    item_name: Mapped[str] = mapped_column(ForeignKey("items.name"))
    item: Mapped["BDItem"] = relationship(back_populates="stats")
    def __repr__(self) -> str:
        return f"Stat(id={self.id!r}, Name={self.name!r}, Value={self.value!r}, Item name={self.item_name!r})"

class BDUser(Base):
    __tablename__ = "users"
    user_name: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(String())
    active: Mapped[bool] = mapped_column(Boolean)
    def __repr__(self) -> str:
        return f"Username(id={self.user_name!r}, Active={self.active!r})"
