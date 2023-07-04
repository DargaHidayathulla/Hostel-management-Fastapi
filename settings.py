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
    prefix="/Settings",
    tags=["SETTINGS"],
    responses={404:{"description":"not found"}}
)
models.Base.metadata.create_all(bind=engine)
def get_db():
    try: 
        db=SessionLocal()
        yield db
    finally:
        db.close()
@router.get("/")
async def raed_all( user:dict=Depends(get_current_user),
                     db:Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    else:
        value=db.query(models.Settings).all()
        value2=db.query(models.Settings).filter(models.Settings.id <6).all()
        user_type=db.query(models.Users)\
                   .filter(models.Users.user_id==user.get("id")).first()
        if user_type. User_type=='owner':
            return value
        elif user_type. User_type=='supervisor':
            return value2 
@router.get("/show")
async def show(user:dict=Depends(get_current_user),
               db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    else:
        new=db.query(models.Users).filter(models.Users.user_id==user.get("id"))
        return{"User_type":new.User_type}