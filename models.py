from sqlalchemy import Boolean,Column,Integer,String,ForeignKey, LargeBinary


from sqlalchemy.orm import relationship
from database import Base

from sqlalchemy.orm import declarative_base, sessionmaker


from datetime import datetime

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    Name=Column(String)
    Phone_Number=Column(String)
    email = Column(String,unique = True,index = True)
    password=Column(String)
    User_type=Column(String)
    companies = relationship("Companies", back_populates="user")
    

class Companies(Base):
    __tablename__="companies"
    Company_id=Column(Integer,primary_key=True,index=True)
    CompanyName=Column(String)
    ContactName=Column(String)
    ContactNumber=Column(String)
    Email=Column(String,unique = True,index = True)
    Address = Column(String)
    City = Column(String)
    State=Column(String)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    user = relationship("Users", back_populates="companies")
    hostels = relationship("Hostels",back_populates="Company")
    
class Hostels(Base):
    __tablename__ = "hostels"
    Hostel_id = Column(Integer, primary_key=True, index=True)
    HostelName = Column(String)
    Hosteltype = Column(String)
    ContactNumber = Column(String)
    Address1 = Column(String)
    Address2 = Column(String)
    City = Column(String)
    State = Column(String)
    PinCode = Column(Integer)
    Company_id = Column(Integer, ForeignKey("companies.Company_id"))
    Company = relationship("Companies", back_populates="hostels")
    supervisor=relationship("UserHostelMap",back_populates="hostel")
    roomrates=relationship("RoomRates",back_populates="hostelname")
    rooms=relationship("Rooms",back_populates="hostelname")
    roomtype=relationship("RoomType",back_populates="hostel")
    customers=relationship("Customers",back_populates="hostelname1")
class UserHostelMap(Base):
    __tablename__ = "userhostelmap"

    id = Column(Integer, primary_key=True, index=True)
    Supervisor_id = Column(Integer)
    Hostel_id = Column(Integer, ForeignKey("hostels.Hostel_id"))
    
   
    hostel= relationship("Hostels", back_populates="supervisor")


class Settings(Base):
    __tablename__="settings"
    id=Column(Integer,primary_key=True,index=True)
    Title=Column(String)
    Description=Column(String)
  

class RoomRates(Base):
    __tablename__="roomrates"
    id=Column(Integer,primary_key=True,index=True)
    RoomType=Column(String)
    Hostel_id = Column(Integer, ForeignKey("hostels.Hostel_id"))
    PriceWithFood=Column(Integer)
    PriceWithoutFood=Column(Integer)
    HostelName=Column(String)
    hostelname=relationship("Hostels",back_populates="roomrates")

class RoomType(Base):
    __tablename__="roomtype"
    id=Column(Integer,primary_key=True,index=True)
    RoomType=Column(String)
    BedCount=Column(Integer)
    HostelName=Column(String)
    Hostel_id = Column(Integer, ForeignKey("hostels.Hostel_id"))
    hostel = relationship("Hostels", back_populates="roomtype")
     
class Rooms(Base):
    __tablename__="rooms"
    id=Column(Integer, primary_key=True,index=True)
    RoomNumber=Column(String)
    RoomType=Column(String)
    PriceWithFood=Column(Integer)
    PriceWithoutFood=Column(Integer)  # Added this column
    NumberofBeds=Column(String)
    HostelName=Column(String)
    Hostel_id = Column(Integer, ForeignKey("hostels.Hostel_id"))
    hostelname=relationship("Hostels",back_populates="rooms")
    beds=relationship("Beds",back_populates="bedsname")

class Beds(Base):
    __tablename__="beds"
    id=Column(Integer, primary_key=True,index=True)
    BedNumber=Column(Integer)
    BedStatus=Column(String)
    Room_id= Column(Integer, ForeignKey("rooms.id"))
    bedsname=relationship("Rooms",back_populates="beds")
    bedsname1=relationship("Tenants",back_populates="tenant")

class Customers(Base):
    __tablename__="customers"
    id=Column(Integer, primary_key=True, index=True)
    CustomerName=Column(String)
    ContactNumber=Column(String,unique = True,index = True)
    Email = Column(String)
    HostelName=Column(String)
    Description=Column(String)
    Hostel_id = Column(Integer, ForeignKey("hostels.Hostel_id"))
    hostelname1=relationship("Hostels",back_populates="customers")


class Tenants(Base):
    __tablename__="tenants"
    id=Column(Integer, primary_key=True, index=True)
    TenantName=Column(String)
    ContactNumber=Column(String)
    Email=Column(String)
    EmergencyNumber=Column(String)
    CheckInDate=Column(String)
    Address=Column(String)
    Area=Column(String)
    City=Column(String)
    State=Column(String)
    PinCode=Column(String)
    HostelName=Column(String)
    RoomType=Column(String)
    RoomNumber=Column(String)
    BedNumber=Column(String)
    Bed_id=Column(Integer, ForeignKey("beds.id"))
    tenant=relationship("Beds",back_populates="bedsname1")
    tenant1=relationship("Document",back_populates="file")


class Document(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    DocType = Column(String)
    data = Column(LargeBinary)
    Tenant_id=Column(Integer, ForeignKey("tenants.id"))
    file=relationship("Tenants",back_populates="tenant1")
