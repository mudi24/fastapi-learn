from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    price = Column(Float)
    description = Column(String, nullable=True)
    create_time = Column(DateTime, default=datetime.datetime.now)