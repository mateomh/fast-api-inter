from fastapi import Depends, HTTPException, Path, status, APIRouter
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import CreateUserRequest, get_current_user
from database import SessionLocal
from models import Users

router = APIRouter(
  tags=['Users'],
  prefix='/users'
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class PasswordRequest(BaseModel):
  password: str
  new_password: str = Field(min_length=6)


class UpdateUserInformationRequest(BaseModel):
  email: str
  first_name: str
  last_name: str
  phone_number: str


@router.get('/me', status_code=status.HTTP_200_OK)
def get_user_info(db: db_dependency, user: user_dependency):
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details='Not Logged In')

  return db.query(Users).filter(Users.id == user.get('id')).first()


@router.post('/password', status_code=status.HTTP_204_NO_CONTENT)
def change_password(db: db_dependency, user: user_dependency, req: PasswordRequest):
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details='Not Logged In')

  curr_user = db.query(Users).filter(Users.id == user.get('id')).first()
  
  if not bcrypt_context.verify(req.password, curr_user.hashed_password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details='Authentication failed') 

  curr_user.hashed_password = bcrypt_context.hash(req.new_password)

  db.add(curr_user)
  db.commit

@router.put('/information', status_code=status.HTTP_204_NO_CONTENT)
def update_user_information(db: db_dependency, user: user_dependency, req: UpdateUserInformationRequest):
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details='Not Logged In')

  curr_user = db.query(Users).filter(Users.id == user.get('id')).first()
  curr_user.email = req.email
  curr_user.first_name = req.first_name
  curr_user.last_name = req.last_name
  curr_user.phone_number = req.phone_number

  db.add(curr_user)
  db.commit    