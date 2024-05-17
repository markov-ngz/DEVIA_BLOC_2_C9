import datetime
from typing import List
from xmlrpc.client import SERVER_ERROR
from sqlalchemy import  Column, DateTime, ForeignKey, Integer, String, Table, text
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True)
    email : Mapped[str] = mapped_column(nullable=False, unique= True)
    password: Mapped[str] = mapped_column(nullable=False)
    phone_number : Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),nullable=False, server_default=text('now()'))
    last_login: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),nullable=False, server_default=text('now()'))
    
