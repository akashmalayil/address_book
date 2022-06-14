from unicodedata import numeric
from pydantic import BaseModel
from sqlalchemy import Numeric

class AddressBook(BaseModel):
    address: str
    city: str
    country: str
    zip_code: str
    state: str
    latitude: float
    longitude: float


class ShowAddressBook(AddressBook):
    class Config():
        orm_mode = True