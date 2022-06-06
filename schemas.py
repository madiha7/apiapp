from pydantic import BaseModel

# Create Address Schema (Pydantic Model)
class AddressCreate(BaseModel):
    name: str
    latitude: float
    longitude: float

# Complete Address Schema (Pydantic Model)
class Address(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True 