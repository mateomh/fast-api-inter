from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from database import SessionLocal
from jose import JWTError, jwt
from models import Users
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated

SECRET_KEY = 'eed626ae447fef9cab8c71472a73fb5de3cfc9b8f951b821c47bb5441bbdec66'
ALGORITHM = 'HS256'

router = APIRouter(
  prefix='/auth',
  tags=['Auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


db_dependency = Annotated[Session,Depends(get_db)]


class CreateUserRequest(BaseModel):
  username: str
  email: str
  first_name: str
  last_name: str
  password: str
  role: str


class Token(BaseModel):
  access_token: str
  token_type: str


@router.post('/', status_code=status.HTTP_201_CREATED)
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

def authenticate_user(username: str, password: str, db):
  user = db.query(Users).filter(username == Users.username).first()
  if user is None:
    return False
  
  if not bcrypt_context.verify(password, user.hashed_password):
    return False
  
  return user


def create_access_token(username: str, user_id: str, role: str, expires_delta: timedelta):
  jwt_data = {
    "sub": username,
    "id": user_id,
    "role": role
  }

  expires = datetime.now(timezone.utc) + expires_delta

  jwt_data.update({ "exp": expires })

  return jwt.encode(jwt_data, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
  try:
    payload =jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get('sub')
    user_id: int = payload.get('user_id')
    role: str = payload.get('role')

    if username is None or user_id is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Can't validate user")
    
    return { "username": username, "id": user_id, "user_role": role }
  except JWTError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Can't validate user")


@router.post('/token', response_model=Token)
def login_for_access_token(
  form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
  db: db_dependency
):
  user_authenticated = authenticate_user(form_data.username, form_data.password, db)

  if not user_authenticated:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed authentication')

  token = create_access_token(user_authenticated.username, user_authenticated.id, user_authenticated.role, timedelta(minutes=20))

  return { "access_token": token, "token_type": "Bearer" }