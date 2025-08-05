from typing import Annotated
from fastapi import APIRouter, Depends, status
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CreateUserRequest(BaseModel):
  username: str
  email: str
  first_name: str
  last_name: str
  password: str
  role: str


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependency = Annotated[Session,Depends(get_db)]


@router.post('/auth', status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, req: CreateUserRequest):
  user = Users(
    username=req.username,
    email=req.email,
    first_name=req.first_name,
    last_name=req.last_name,
    role=req.role,
    hashed_password=bcrypt_context.hash(req.password)
  )

  db.add(user)
  db.commit()

  return user