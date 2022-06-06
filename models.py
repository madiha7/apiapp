from sqlalchemy import Column, Integer, String, Float
from database import Base

# Define To Do class inheriting from Base
class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    name = Column("level", String(50))
    latitude = Column(Float)
    longitude = Column(Float)