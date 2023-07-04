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
from sqlalchemy.orm import joinedload

router=APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404:{"description":"not found"}}
)
models.Base.metadata.create_all(bind=engine)
def get_db():
    try: 
        db=SessionLocal()
        yield db
    finally:
        db.close()

class Users(BaseModel):
    Name:str
    Phone_Number:str
    email:str
    password:str
    hostel:list

    


@router.post("/create")
async def create(users: Users,  # accept a list of hostel names
                             user: dict = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    supervisor = models.Users()
    supervisor.Name=users.Name
    supervisor.Phone_Number=users.Phone_Number
    supervisor.email=users.email
    supervisor.password=users.password
    supervisor.User_type = "supervisor"

    db.add(supervisor)
    db.commit()
    db.flush


    for hostels in users.hostel:
        c=db.query(models.Hostels).filter(models.Hostels.HostelName==hostels)\
        .filter(models.Companies.user_id==user.get("id")).first()

        mapping=models.UserHostelMap()
        new=db.query(models.Users).order_by(models.Users.user_id.desc()).first()
        mapping.Supervisor_id=new.user_id
        mapping.Hostel_id=c.Hostel_id
        db.add(mapping)
        db.commit()
        db.flush()
    return {"message": "Supervisor created successfully "}
@router.put("/edit_user/{id}")
async def edit(id: int, users: Users,
               user: dict = Depends(get_current_user),
               db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    # Get the supervisor to edit from the database
    supervisor = db.query(models.Users)\
                   .filter(models.Users.user_id == id)\
                   .filter(models.Users.User_type == "supervisor")\
                   .first()

    if not supervisor:
        return {"message": "Supervisor not found"}

    # Update the supervisor's attributes
    supervisor.Name = users.Name
    supervisor.Phone_Number = users.Phone_Number
    supervisor.email = users.email
    supervisor.password = users.password
    db.add(supervisor)
    db.commit()

    # Update the supervisor's hostel mappings
    db.query(models.UserHostelMap)\
      .filter(models.UserHostelMap.Supervisor_id == supervisor.user_id)\
      .delete()

    for hostelname in users.hostel:
        hostel = db.query(models.Hostels)\
                   .filter(models.Hostels.HostelName == hostelname)\
                   .filter(models.Companies.user_id == user.get("id"))\
                   .first()

        if not hostel:
            return {"message": f"Hostel '{hostelname}' not found"}

        mapping = models.UserHostelMap()
        mapping.Supervisor_id = supervisor.user_id
        mapping.Hostel_id = hostel.Hostel_id
        db.add(mapping)
        db.commit()
        db.flush()

    return {"message": "Supervisor edited successfully"}


    
@router.get("/show_hostel")
async def show_hostels_by_supervisor(user:dict=Depends(get_current_user),
                                     db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return db.query(models.Hostels).filter(models.Hostels.Hostel_id==models.UserHostelMap.Hostel_id)\
           .filter(models.UserHostelMap.Supervisor_id==user.get("id")).all()

@router.get("/show_user")
async def show_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    new=db.query(models.Users).filter(models.Users.user_id==user.get("id")).first()
    if new.User_type == "admin":
        # return all users of type owner
        return db.query(models.Users).filter(models.Users.User_type == 'owner').all()
    elif new.User_type == "owner":
        # return all supervisors associated with the hostels owned by the owner
        supervisors = db.query(models.Users).filter(
            models.Users.User_type == 'supervisor'
        ).join(
            models.UserHostelMap,
            models.UserHostelMap.Supervisor_id == models.Users.user_id
        ).join(
            models.Hostels,
            models.Hostels.Hostel_id == models.UserHostelMap.Hostel_id
        ).join(
            models.Companies,
            models.Companies.Company_id == models.Hostels.Company_id
        ).filter(
            models.Companies.user_id == user.get("id")
        ).all()
        l=[]

        # for each supervisor, also fetch the hostels assigned to them
        for supervisor in supervisors:
            supervisor.hostels = db.query(models.Hostels).join(
                models.UserHostelMap,
                models.UserHostelMap.Hostel_id == models.Hostels.Hostel_id
            ).filter(
                models.UserHostelMap.Supervisor_id == supervisor.user_id
            ).all()
            l.append(supervisor)
        return l 

    # hostel_ids = []  # to store the hostel IDs

    # for hostelname in users.hostelname:
    #     # Retrieve the hostel ID based on the hostel name
    #     hostel_row = db.query(models.Hostels.hostel_id)\
    #         .filter(models.Hostels.hostelname == hostelname).first()
    #     if hostel_row is None:
    #         raise HTTPException(status_code=404, detail=f"Hostel name '{hostelname}' not found")
    #     hostel_ids.append(hostel_row[0])  # Extract the integer value from the Row object

    # # Create mappings between supervisor and hostels
    # for hostel_id in hostel_ids:
    #     mapping = models.Hostelmapping()
    #     mapping.supervisor_id = supervisor.id
    #     mapping.hostel_id = hostel_id
    #     db.add(mapping)

    # db.commit()
    # return {"message": "Supervisor created successfully "}