from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import List
from db.session import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    Username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(100))

    def __repr__(self)->str:
        return f"User(id={self.id}, Username={self.Username}, email={self.email}, password={self.password})"

class Data(Base):
    __tablename__ = 'data'
    id: Mapped[int] = mapped_column(primary_key=True,)
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column(String(50))
    rollno: Mapped[int] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))

    def __repr__(self)->str:
        return f"User(id={self.id}, name={self.name}, age={self.age}, rollno={self.rollno}, email={self.email})"