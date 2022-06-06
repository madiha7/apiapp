from ctypes import addressof
from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
from math import cos, asin, sqrt, pi 

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/")
def root():
    return "Adresses"

@app.post("/address", response_model=schemas.Address, status_code=status.HTTP_201_CREATED)
def create_address(address: schemas.AddressCreate, session: Session = Depends(get_session)):

    # create an instance of the Address database model
    addressdb = models.Address(name = address.name, latitude = address.latitude, longitude = address.longitude)
    
    # Validate the latitude and longitude of the address
    if addressdb.latitude not in [-90.0, 90.0] or  addressdb.longitude not in [-180.0, 180.0]:
        raise HTTPException(status_code=400, detail=f"Invalid address. Please provide Latitude in range [-90.0, 90.0] and Longitude in range [-180.0, 180.0].")
    
    # add it to the session and commit it
    session.add(addressdb)
    session.commit()
    session.refresh(addressdb)

    # return the address object
    return addressdb

@app.get("/address/{id}", response_model=schemas.Address)
def read_address(id: int, session: Session = Depends(get_session)):

    # get the address item with the given id
    address = session.query(models.Address).get(id)

    # check if address item with given id exists. If not, raise exception and return 404 not found response
    if not address:
        raise HTTPException(status_code=404, detail=f"address item with id {id} not found")

    return address

@app.put("/address/{id}", response_model=schemas.Address)
def update_address(id: int, name: str, latitude: float, longitude: float, session: Session = Depends(get_session)):

    # get the address item with the given id
    address = session.query(models.Address).get(id)

    # update address item with the given task (if an item with the given id was found)
    if address:
        address.name = name
        address.latitude = latitude
        address.longitude = longitude
        session.commit()

    # check if address item with given id exists. If not, raise exception and return 404 not found response
    if not address:
        raise HTTPException(status_code=404, detail=f"address item with id {id} not found")

    return address

@app.delete("/address/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(id: int, session: Session = Depends(get_session)):

    # get the address item with the given id
    address = session.query(models.Address).get(id)

    # if address item with given id exists, delete it from the database. Otherwise raise 404 error
    if address:
        session.delete(address)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"address item with id {id} not found")

    return None

@app.get("/address", response_model = List[schemas.Address])
def read_address_list(session: Session = Depends(get_session)):

    # get all address items
    address_list = session.query(models.Address).all()

    return address_list 

@app.put("/address", response_model = List[schemas.Address])
def neighbours_address_list( latitude :float, longitude: float, distance: float, session: Session = Depends(get_session)):
    
    # get all address items
    address_list = session.query(models.Address).all()

    neighbours_list=[] # empty list to collect all the addresses with given distance 

    lat2 = latitude  
    lon2 = longitude # Given by the user

    for address in address_list: 

        lat1 = address.latitude
        lon1 = address.longitude
        
        p = pi/180 # in radians
        r = 6371  # Earth's Radius

        # Formula to calculate the distance between two objects
        
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
        
        d = 2 * r * asin(sqrt(a))
        
        if d <= distance:
            neighbours_list.append(address)

    # If there are no addresses within give distance and coordinates return appropriate message.      
    if not neighbours_list:
        return f"There are no Addresses in the Address List within {distance} KM"

    # Return the addresses which lie within given distance
    return neighbours_list