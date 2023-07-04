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
import random
import smtplib
import string
router=APIRouter(
    prefix="/companies",
    tags=["Companies"],
    responses={404:{"description":"not found"}}
)
models.Base.metadata.create_all(bind=engine)
def get_db():
    try: 
        db=SessionLocal()
        yield db
    finally:
        db.close()
class Company(BaseModel):
    CompanyName:str
    ContactName:str
    Email:str
    ContactNumber:str
    Address : str
    City:str
    State:str



@router.get("/show")
async def show_companies(user:dict=Depends(get_current_user),
                           db:Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    new=db.query(models.Users)\
                   .filter(models.Users.user_id==user.get("id")).first()
    if   new.User_type=='owner':
            return db.query(models.Companies)\
               .filter(models.Companies.user_id == user.get("id"))\
               .all()
    elif new.User_type=='admin':
            return db.query(models.Companies).all()

@router.post("/create")
async def create_companies(companies:Company,
                    user:dict=Depends(get_current_user),
                    db:Session=Depends(get_db)):
    if user is None:

        raise get_user_exception()
    user_model= models.Users()
    user_model.Name=companies.ContactName
    user_model.Phone_Number=companies.ContactNumber
    user_model.email=companies.Email
    pas=new_password(companies.Email)
    user_model.password=pas
    user_model.User_type="owner"
    db.add(user_model)
    db.commit()
    db.flush
    company_model = models.Companies()
    company_model.CompanyName= companies.CompanyName
    company_model.ContactName=companies.ContactName
    company_model.Email = companies.Email
    company_model.ContactNumber =companies.ContactNumber
    company_model.Address = companies.Address
    company_model.City = companies.City
    company_model.State=companies.State
    new=db.query(models.Users).order_by(models.Users.user_id.desc()).first()
    company_model.user_id=new.user_id
 
    db.add(company_model)
    db.commit()
    db.flush
    return sucessful_response(201)
def new_password(email):      
        otp = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('dargahidayathulla639@gmail.com','aopcknewsarbnqsi')
        msg='Hello, Your OTP is '+str(otp)
        server.sendmail('dargahidayathulla639@gmail.com',email,msg)
        server.quit()
        return otp

@router.put("/edit_company/{id}")
async def edit_companies(id:int,companies:Company,
                    user:dict=Depends(get_current_user),
                    db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    company_model=db.query(models.Companies)\
        .filter(models.Companies.Company_id==id)\
        .filter(models.Companies.user_id == user.get("id"))\
        .first()
    if company_model is  None:
        raise http_exception()
    company_model.CompanyName =companies.CompanyName
    company_model.ContactName=companies.ContactName
    company_model.Email = companies.Email
    company_model.ContactNumber =companies.ContactNumber
    company_model.Email = companies.Email
    company_model.Address = companies.Address
    company_model.City = companies.City
    company_model.State=companies.State
    db.add(company_model)
    db.commit()
    return " updated sucessfully"

def sucessful_response(status_code:int):
    return{
        'status':status_code,
        'transaction':'sucessful'
    }
def http_exception():
    return HTTPException(status_code=404,detail="company not found")
# @router.get("/show")
# async def show_companies(db:Session=Depends(get_db)):
#     return db.query(models.Companies).all()