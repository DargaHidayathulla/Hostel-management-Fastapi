import sys
sys.path.append( "..")
import random
import smtplib
import string
from email.mime.text import MIMEText
from typing import Optional
from fastapi import Depends ,HTTPException,APIRouter,Request
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from fastapi.responses import HTMLResponse
from .auth import get_current_user,get_user_exception

from fastapi import  APIRouter,FastAPI, Depends
router=APIRouter(
    prefix="/auth",
    tags=["authorization"],
    responses={404:{"description":"not found"}}
)
models.Base.metadata.create_all(bind=engine)

def get_db():
    try: 
        db=SessionLocal()
        yield db
    finally:
        db.close()
class Email(BaseModel):
     email:str
class changepassword(BaseModel):
     current_password:str
     new_password:str
     confirm_password:str   
@router.put("/change_password")
async def change_password(password:changepassword, user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    user_db = db.query(models.Users).filter(models.Users.user_id== user.get("id")).first()
    if user_db is None:
        return{"msg":"User not found"}
    if password.current_password!=user_db.password:
        return{"msg":"Invalid current password"}
    if password.new_password != password.confirm_password:
        return{"msg":"New password and confirm password do not match"}
    user_db.password=(password.new_password)
    db.add(user_db)
    db.commit()
    return {"msg": "Password changed successfully"}





@router.post('/forgot_password')
async def forgot_password(email:Email,db:Session=Depends(get_db)):
    mail=email.email
    new =db.query(models.Users).filter(models.Users.email==mail).first()
    if new is None:
        return{"invalid":"invalid email"}
    elif new  is not None:
        pas=new_password(mail)
        new.password = pas
    db.commit()
    return {"success":"password changed sucessfully"}    
def new_password(email):      
        otp = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('dargahidayathulla639@gmail.com','aopcknewsarbnqsi')
        msg='Hello, Your OTP is '+str(otp)
        server.sendmail('dargahidayathulla639@gmail.com',email,msg)
        server.quit()
        return otp
