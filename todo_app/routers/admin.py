from fastapi import Depends, HTTPException, Path, status, APIRouter
from pydantic import BaseModel, Field
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user
from models import Todos

router = APIRouter(
  prefix='/admin',
  tags=['Admin']
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/todo', status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):
  if user is None or user.get('user_role') != 'admin':
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
  
  todos = db.query(Todos).all()

  return todos


@router.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_dependency, db: db_dependency, todo_id: int=Path(gt=0)):
  if user is None or user.get('user_role') != 'admin':
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details='Authentication failed')

  todo = db.query(Todos).filter(Todos.id == todo_id)

  if todo is None:
    raise HTTPException(status_code=404, detail='Todo not found')
  
  todo.delete()
  db.commit()

