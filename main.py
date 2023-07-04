from fastapi import FastAPI
from routers import auth
from routers import sample
from routers import companies
from routers import hostels
from routers import users
from routers import settings
from routers import roomrates
from routers import roomtype
from routers import rooms
from routers import customers
from routers import tenants
# from routers import images
from database import engine
import models
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
models.Base.metadata.create_all(bind=engine)
app=FastAPI()


origins = [
    # "http://localhost:4200"
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(sample.router)
app.include_router(companies.router)
app.include_router(hostels.router)
app.include_router(users.router)
app.include_router(settings.router)
app.include_router(roomrates.router)
app.include_router(roomtype.router)
app.include_router(rooms.router)
app.include_router(customers.router)
app.include_router(tenants.router)
# app.include_router(images.router)
# if __name__=="__main__":
#     uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)