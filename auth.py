import sys
sys.path.append( "..")
from fastapi import Depends,HTTPException,status,APIRouter,Request,Response
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal,engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime,timedelta
from jose import jwt,JWTError


SECRET_KEY ="KlgH6AzYDeZeGwD288to 79I3vTHT8wp7" 
ALGORITHM = "HS256" 
bcrypt_context =CryptContext(schemes=["bcrypt"],deprecated="auto")
models.Base.metadata.create_all(bind=engine)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/auth",
    tags=["authorization"],
    responses={401:{"user":"not authorized"}}
)

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()
def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password,hashed_password):
    if plain_password==hashed_password:
        return True
    else:
        return False

def authenticate_user(email:str,password:str,db):
    user = db.query(models.Users)\
       .filter(models.Users.email == email )\
       .first()
    if not user:
        return False
    if not verify_password(password,user.password):
        return False
    return user


def create_access_token(username:str,user_id:int,
                        expires_delta:Optional[timedelta]=None):
    encode = {"sub":username,"id":user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=360)
    encode.update({"exp":expire})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(token:str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get("sub")
        user_id:int =payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return{"username":username,"id":user_id}
    except JWTError:
        raise get_user_exception()

class login(BaseModel):
    username:str
    password:str
@router.post("/login")
async def login_for_access_token(data:login,db:Session = Depends(get_db)):
    user = authenticate_user(data.username,data.password,db)
    if not user:
        return{"msg": "incorrect  username" }
        # raise token_exception()
    token_expires = timedelta(minutes=360)
    token = create_access_token(user.email,
                                user.user_id,
                                expires_delta=token_expires)
    
    return{"token":token,"User":"User Found"}
@router.get('/user')
async def get_user(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    user_model=db.query(models.Users).filter(models.Users.user_id==user.get("id")).first()
    if user_model is None:
        return "invalid user_id"
    else:
         return {'name':user_model.Name,'email':user_model.email,'User_type':user_model.User_type}

def get_user_exception():
    credentials_exception =HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    return credentials_exception
def token_exception():
    token_exception_response =HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="incorrect username or password",
    headers={"WWW-Authenticate":"Bearer"}
    )
    return token_exception_response
        
       

    
