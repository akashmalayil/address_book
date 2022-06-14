from decimal import Decimal
import imp
import sqlalchemy
from .database import Base
from sqlalchemy import Column, Integer, String, DECIMAL

class AddressBook(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    city = Column(String)
    country = Column(String)
    zip_code = Column(String)
    state = Column(String)
    latitude = Column(DECIMAL(8,6))
    longitude = Column(DECIMAL(9,6))