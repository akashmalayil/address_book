from typing import List
from urllib import request, response
from fastapi import FastAPI, Depends, Response, status, HTTPException
from . import schemas
from . import models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Address
@app.post("/address", status_code=status.HTTP_201_CREATED)
def create(request: schemas.AddressBook, db : Session = Depends(get_db)):
    new_address = models.AddressBook(address = request.address, city = request.city, country = request.country, zip_code = request.zip_code, state = request.state, latitude = request.latitude, longitude = request.longitude)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

# Update Address
@app.put("/address/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.AddressBook, db : Session = Depends(get_db)):
    blog = db.query(models.AddressBook).filter(models.AddressBook.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Address with the id {id} does not exist")
    blog.update({"address":request.address,"city":request.city,"country":request.country,"zip_code":request.zip_code,"state":request.state,"latitude":request.latitude,"longitude":request.longitude})
    db.commit()
    return 'Updated'

# Delete address by id
@app.delete("/address/{id}",status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, response: Response, db : Session = Depends(get_db)):
    db.query(models.AddressBook).filter(models.AddressBook.id == id).delete(synchronize_session=False)
    db.commit()
    return "Deleted"

# Get all address 
@app.get("/address",response_model=List[schemas.ShowAddressBook])
def all(db : Session = Depends(get_db)):
    addresses = db.query(models.AddressBook).all()
    return addresses

# Get address by id
@app.get("/address/{id}",status_code=status.HTTP_200_OK, response_model=schemas.ShowAddressBook)
def show(id:int, db : Session = Depends(get_db)):
    address = db.query(models.AddressBook).filter(models.AddressBook.id == id).first()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"Address with the id {id} does not exist")
    return address

# Get address by id
@app.get("/search",status_code=status.HTTP_200_OK, response_model=List[schemas.ShowAddressBook])
def show(latitude:float=0,longitude:float=0,distance:float=0,db : Session = Depends(get_db)):
    query = db.query(models.AddressBook)
    if distance > 0:
        cordinates_diff = distance/111
        p_latitude = latitude + cordinates_diff
        p_longitude = longitude + cordinates_diff
        n_latitude = latitude - cordinates_diff
        n_longitude = longitude - cordinates_diff
        addresses = query.filter(models.AddressBook.latitude >= n_latitude, models.AddressBook.longitude >= n_longitude, models.AddressBook.latitude <= p_latitude, models.AddressBook.longitude <= p_longitude).all()
    else:
        addresses = query.filter(models.AddressBook.latitude == latitude, models.AddressBook.longitude == longitude).all()

    if not addresses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"No record found")
    return addresses