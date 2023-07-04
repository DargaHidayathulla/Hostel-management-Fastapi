import sys
sys.path.append("..")
from typing import Optional
from fastapi import Depends,APIRouter,Form,HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from fastapi.responses import HTMLResponse
from .auth import get_current_user,get_user_exception
router=APIRouter(
    prefix="/roomrates",
    tags=["ROOMRATES"],
    responses={404:{"description":"not found"}}
)
models.Base.metadata.create_all(bind=engine)
def get_db():
    try: 
        db=SessionLocal()
        yield db
    finally:
        db.close()


class Room(BaseModel):
    RoomType:str
    HostelName:str
    PriceWithFood:int
    PriceWithoutFood:int

@router.post("/create")
async def create_roomrates(roomrates: Room, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

   
    # Create and save the new RoomRates object
    room_model = models.RoomRates()
    room_model.RoomType = roomrates.RoomType
    room_model.PriceWithFood = roomrates.PriceWithFood
    room_model.PriceWithoutFood = roomrates.PriceWithoutFood
    room_model.HostelName = roomrates.HostelName
    new = db.query(models.Hostels).filter(models.Hostels.HostelName == roomrates.HostelName)\
        .filter(models.Companies.Company_id == models.Hostels.Company_id)\
        .filter(models.Companies.user_id == user.get("id"))\
        .first()
    room_model.Hostel_id = new.Hostel_id
     # Check if a RoomRates object with the same RoomType and Hostel_id already exists
    room3 = db.query(models.RoomRates).filter(models.RoomRates.RoomType ==roomrates.RoomType)\
                            .filter(models.RoomRates.Hostel_id==room_model.Hostel_id).first()
    if room3 is  not None:
        if roomrates.RoomType==room3.RoomType:
            return {"error": "A RoomRates with the same RoomType and Hostel_id already exists"}

    db.add(room_model)
    db.commit()
    return {"message": "RoomRates created"}


@router.get("/show")
async def show_user(user:dict=Depends(get_current_user),
                    db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    new=db.query(models.Users).filter(models.Users.user_id==user.get("id")).first()
    if new.User_type=="owner":
        return db.query(models.RoomRates).filter(models.RoomRates.Hostel_id==models.Hostels.Hostel_id)\
                      .filter(models.Companies.Company_id==models.Hostels.Company_id)\
                      .filter(models.Companies.user_id==user.get("id")).all()

@router.put("/edit/{id}")
async def edit(id: int, roomrates: Room, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    # Get the RoomRates object by id
    room_model = db.query(models.RoomRates)\
                   .filter(models.RoomRates.id == id)\
                   .first()
    
    # Raise an HTTPException if the room is not found
    if room_model is None:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Update the RoomRates object attributes
    # room_model.RoomType = roomrates.RoomType
    # new = db.query(models.Hostels)\
    #         .filter(models.Hostels.HostelName == roomrates.HostelName)\
    #         .filter(models.Companies.Company_id == models.Hostels.Company_id)\
    #         .filter(models.Companies.user_id == user.get("id"))\
    #         .first()
    # room_model.Hostel_id = new.Hostel_id
    # room_model.HostelName = roomrates.HostelName
    room_model.PriceWithFood = roomrates.PriceWithFood
    room_model.PriceWithoutFood = roomrates.PriceWithoutFood
    
    # Add the RoomRates object to the session and commit the changes
    db.add(room_model)
    db.commit()
    return("roomrates updated")
