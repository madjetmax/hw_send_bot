from sqlalchemy import DateTime, Float, String, Text, Boolean, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(Text)
    send_home_work_daily: Mapped[bool] = mapped_column(Boolean, default=True)

class Day(Base):
    __tablename__ = "day"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    home_work: Mapped[str] = mapped_column(Text, default="[]")

class BotData(Base):
    __tablename__ = "botData"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    admins: Mapped[str] = mapped_column(Text, default="[859261869]") 
    send_home_work_daily_for_all_users: Mapped[bool] = mapped_column(Boolean, default=True)
