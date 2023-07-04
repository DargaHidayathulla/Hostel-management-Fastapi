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
    prefix="/roomtypes",
    tags=["ROOMTYPES"],
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
    BedCount:int
    HostelName:str

@router.post("/create")
async def create_roomrates(roomtype:Room,
                            user:dict=Depends(get_current_user),
                            db:Session=Depends(get_db)):
    if user is None:
         raise get_user_exception()
    # new=db.query(models.Users).filter(models.Users.user_id==user.get("id"))\
    #            .first()
    
    room_model=models.RoomType()
    room_model.RoomType=roomtype.RoomType
    room_model.BedCount=roomtype.BedCount
    room_model.HostelName=roomtype.HostelName
    new=db.query(models.Hostels).filter(models.Hostels.HostelName==roomtype.HostelName)\
              .filter(models.Companies.Company_id==models.Hostels.Company_id)\
              .filter(models.Companies.user_id==user.get("id"))\
              .first()
    room_model.Hostel_id= new.Hostel_id
    room3 = db.query(models.RoomType).filter(models.RoomType.RoomType ==roomtype.RoomType)\
                            .filter(models.RoomType.Hostel_id==room_model.Hostel_id).first()
    if room3 is  not None:
        if roomtype.RoomType==room3.RoomType:
            return {"error": "A Roomtype with the same RoomType and Hostel_id already exists"}

    db.add(room_model)
    db.commit()
    return("roomtype created")


@router.put("/edit/{id}")
async def edit(id:int,roomtype:Room,
                  user:dict=Depends(get_current_user),
                db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    room_model=db.query(models.RoomType)\
                .filter(models.RoomType.id==id)\
                .first()                      
    room_model.RoomType=roomtype.RoomType
    room_model.BedCount=roomtype.BedCount
    # room_model.user_id=user.get("id")
    db.add(room_model)
    db.commit()
    return("roomtype updated")


@router.get("/show")
async def show_user(user:dict=Depends(get_current_user),
                    db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    new=db.query(models.Users).filter(models.Users.user_id==user.get("id")).first()
    if new.User_type=="owner":
        return db.query(models.RoomType).filter(models.RoomType.Hostel_id==models.Hostels.Hostel_id)\
                      .filter(models.Companies.Company_id==models.Hostels.Company_id)\
                      .filter(models.Companies.user_id==user.get("id")).all()