import sys
sys.path.append("..")
from typing import Optional
from fastapi import Depends,APIRouter,File,UploadFile,HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from fastapi.responses import HTMLResponse,JSONResponse

from .auth import get_current_user,get_user_exception
router=APIRouter(
    prefix="/customers",
    tags=["Customers"],
    responses={404:{"description":"not found"}}
)
models.Base.metadata.create_all(bind=engine)
def get_db():
    try: 
        db=SessionLocal()
        yield db
    finally:
        db.close()
class Customer(BaseModel):
    CustomerName:str
    ContactNumber:str
    Email:str
    HostelName:str
    Description:str
   
@router.post("/create")
async def create_customers(customer:Customer,
                    user:dict=Depends(get_current_user),
                    db:Session=Depends(get_db)):
    if user is None:
       raise get_user_exception()
    customer_model=models.Customers()
    customer_model.CustomerName=customer.CustomerName
    customer_model.ContactNumber=customer.ContactNumber
    customer_model.Email=customer.Email
    customer_model.HostelName=customer.HostelName
    customer_model.Description=customer.Description
    new = db.query(models.Hostels).filter(models.Hostels.HostelName == customer.HostelName)\
        .filter(models.Companies.Company_id == models.Hostels.Company_id)\
        .filter(models.Companies.user_id == user.get("id"))\
        .first()
    customer_model.Hostel_id = new.Hostel_id
    db.add(customer_model)
    db.commit()
    return"customers created"
@router.put("/edit_customer/{id}")
async def edit_customer(id:int,customer:Customer,
                    user:dict=Depends(get_current_user),
                    db:Session=Depends(get_db)):
                 
    if user is None:
        raise get_user_exception()
    customer_model = db.query(models.Customers)\
                   .filter(models.Customers.id == id)\
                   .first()
    
    if customer_model is None:
        return'no customer'
    customer_model.CustomerName=customer.CustomerName
    customer_model.ContactNumber=customer.ContactNumber
    customer_model.Email=customer.Email
    customer_model.HostelName=customer.HostelName
    customer_model.Description=customer.Description
    new = db.query(models.Hostels).filter(models.Hostels.HostelName == customer.HostelName)\
        .filter(models.Companies.Company_id == models.Hostels.Company_id)\
        .filter(models.Companies.user_id == user.get("id"))\
        .first()
    customer_model.Hostel_id = new.Hostel_id
    db.add(customer_model)
    db.commit()
    return"customers updated"
    

