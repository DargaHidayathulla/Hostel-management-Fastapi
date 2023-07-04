import sys
sys.path.append("..")
from typing import Optional
from fastapi import Depends,APIRouter,Form,HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from.auth import get_current_user,get_user_exception
router = APIRouter(
    prefix = "/hostels",
    tags =["Hostels"],
    responses={404:{"description":"Not found"}}  
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
class Hostel(BaseModel):
    HostelName:str
    ContactNumber:str
    Hosteltype:str
    Address1:str
    Address2:str
    City:str
    State:str
    PinCode:int
    # Company_id:int

@router.get("/companies_hostels")
async def companies_hostels(user:dict=Depends(get_current_user),
                                     db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    new=db.query(models.Users)\
                   .filter(models.Users.user_id==user.get("id")).first()
    if new.User_type=='owner':

        return db.query(models.Hostels).filter(models.Hostels.Company_id==models.Companies.Company_id)\
               .filter(models.Companies.user_id==user.get("id")).all()
    elif new.User_type=='admin':
        return db.query(models.Hostels).all()

@router.get("/companyname")
async def companyname(user:dict=Depends(get_current_user),
                      db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    else:
        company=db.query(models.Companies)\
               .filter(models.Companies.user_id == user.get("id"))\
               .first()
        return{'Company':company.CompanyName}



@router.post("/create")
async def create_hostels(hostels:Hostel,
                    user:dict=Depends(get_current_user),
                    db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    company = db.query(models.Companies).filter(models.Companies.user_id == user.get('id')).first()
    hostel_model = models.Hostels()
    hostel_model.HostelName=hostels.HostelName
    hostel_model.Hosteltype=hostels.Hosteltype
    hostel_model.ContactNumber =hostels.ContactNumber
    hostel_model.Address1 = hostels.Address1
    hostel_model.Address2=hostels.Address2
    hostel_model.City = hostels.City
    hostel_model.State = hostels.State
    hostel_model.PinCode = hostels.PinCode
    hostel_model.Company_id=company.Company_id
    db.add(hostel_model)
    db.flush()
    db.commit() 
    return sucessful_response(201)

@router.put("/edit_hostel/{id}")
async def edit_hostel(id:int,hostels:Hostel,
                      user:dict=Depends(get_current_user),
                      db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    hostel_model=db.query(models.Hostels)\
        .filter(models.Hostels.Hostel_id==id)\
        .filter(models.Companies.user_id == user.get("id"))\
        .first()
    if hostel_model is None:
        raise http_exception()
    hostel_model.HostelName=hostels.HostelName
    hostel_model.Hosteltype=hostels.Hosteltype
    hostel_model.ContactNumber =hostels.ContactNumber
    hostel_model.Address1 = hostels.Address1
    hostel_model.Address2=hostels.Address2
    hostel_model.City = hostels.City
    hostel_model.State = hostels.State
    hostel_model.PinCode = hostels.PinCode
    db.add(hostel_model)
    db.flush()
    db.commit()
    return "updated sucessfully"
 
def sucessful_response(status_code:int):
    return{
        'status':status_code,
        'transaction':'sucessful'
    }
def http_exception():
    return HTTPException(status_code=404,detail="company not found")
# @router.post("/create")
# async def create_hostels(
#     hostels: Hostel,
#     user: dict = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     if user is None:
#         raise get_user_exception()
    
#     # Check if the user has access to the selected company
#     if hostels.Company_id is not None:
#         company = db.query(models.Companies).filter(
#             models.Companies.user_id == user.get('id'),
#             models.Companies.Company_id == hostels.Company_id
#         ).first()
#         if company is None:
#             raise Exception("User does not have access to the selected company")

#     else:
#         company = db.query(models.Companies).filter(
#             models.Companies.user_id == user.get('id')
#         ).first()

#     hostel_model = models.Hostels()
#     hostel_model.HostelName = hostels.HostelName
#     hostel_model.Hosteltype = hostels.Hosteltype
#     hostel_model.ContactNumber = hostels.ContactNumber
#     hostel_model.Address1 = hostels.Address1
#     hostel_model.Address2 = hostels.Address2
#     hostel_model.City = hostels.City
#     hostel_model.State = hostels.State
#     hostel_model.PinCode = hostels.PinCode
#     hostel_model.Company_id = company.Company_id

#     db.add(hostel_model)
#     db.commit() 

#     return sucessful_response(201)
# @router.get("/show")
# async def read_all_by_hostels(user:dict=Depends(get_current_user),
#                            db:Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()
#     return db.query(models.Hostels)\
#            .filter(models.Companies.Company_id== user.get("id"))\
#             .all()
# company = db.query(models.Companies) \
    #             .filter(models.Companies.user_id == user.get('id')) \
    #             .filter(models.Companies.CompanyName == models.Companies.CompanyName) \
    #             .first()

