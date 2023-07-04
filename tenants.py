import sys
sys.path.append("..")
from typing import Optional
from fastapi import Depends,APIRouter,File,UploadFile,HTTPException,Form
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from fastapi.responses import HTMLResponse,JSONResponse
import csv
import io,openpyxl
import pandas as pd
from .auth import get_current_user,get_user_exception
router=APIRouter(
    prefix="/tenants",
    tags=["TENANTS"],
    responses={404:{"description":"not found"}}
)
models.Base.metadata.create_all(bind=engine)
def get_db():
    try: 
        db=SessionLocal()
        yield db
    finally:
        db.close()
@router.post("/create")
async def create_rooms(TenantName:str=Form(...),ContactNumber:str=Form(...),Email:str=Form(...),EmergencyNumber:str=Form(...),CheckInDate:str=Form(...),Address:str=Form(...),
                       Area:str=Form(...),City:str=Form(...),State:str=Form(...),PinCode:str=Form(...),HostelName:str=Form(...),RoomType:str=Form(...),RoomNumber:str=Form(...),
                       BedNumber:str=Form(...),DocType:str=Form(...),file1: UploadFile = File(...),
                       user:dict=Depends(get_current_user),
                       db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    tenant_model=models.Tenants()
    tenant_model.TenantName=TenantName
    tenant_model.ContactNumber=ContactNumber
    tenant_model.Email=Email
    tenant_model.EmergencyNumber=EmergencyNumber
    tenant_model.CheckInDate=CheckInDate
    tenant_model.Address=Address
    tenant_model.Area=Area
    tenant_model.City=City
    tenant_model.State=State
    tenant_model.PinCode=PinCode
    tenant_model.HostelName=HostelName
    tenant_model.RoomType=RoomType
    tenant_model.RoomNumber=RoomNumber
    tenant_model.BedNumber=BedNumber
    hostel=db.query(models.Hostels).filter(models.Hostels.HostelName==HostelName)\
            .filter(models.Hostels.Company_id==models.Companies.Company_id)\
            .filter(models.Companies.user_id == user.get('id')).first()
    room=db.query(models.Rooms).filter(models.Rooms.RoomNumber==RoomNumber)\
              .filter(models.Rooms.Hostel_id==hostel.Hostel_id)\
              .filter(models.Rooms.RoomType==RoomType)\
              .filter(models.Hostels.Company_id==models.Companies.Company_id)\
              .filter(models.Companies.user_id==user.get('id')).first()
    beds1=db.query(models.Beds).filter(models.Beds.BedNumber==BedNumber)\
           .filter(models.Beds.Room_id==room.id)\
            .filter(models.Hostels.Company_id==models.Companies.Company_id)\
            .filter(models.Companies.user_id==user.get('id')).first()
    tenant_model.Bed_id=beds1.id
    beds1.BedStatus="occupied"
    db.add(tenant_model)
    db.commit()
    bed_model=models.Document()
    bed_model.data=(file1.file.read())
    bed_model.DocType=DocType
    bed_model.Tenant_id=tenant_model.id
    db.add(bed_model)
    db.commit()
    db.refresh(bed_model)
    return{"tenant created"}