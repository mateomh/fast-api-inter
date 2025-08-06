from fastapi import Depends, HTTPException, Path, status, APIRouter
from pydantic import BaseModel, Field
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user
from models import Todos

router = APIRouter(
  tags=['Todos']
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
  title: str = Field(min_length=3)
  description: str = Field(min_length=3, max_length=100)
  priority: int = Field(gt=0, lt=6)
  complete: bool


@router.get('/health-check')
def root_path():
  return { "status": "ok" }


@router.get('/todos', status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):
  return db.query(Todos).filter(Todos.owner_id == user.get('id'))


@router.get('/todos/{todo_id}', status_code=status.HTTP_200_OK)
def get_single_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details='Authentication failed')

  todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()

  if todo is not None:
    return todo
    
  raise HTTPException(status_code=404, detail='Todo not found')


@router.post('/todos', status_code=status.HTTP_201_CREATED)
def create_todo(user: user_dependency, db: db_dependency, req: TodoRequest):
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details='Authentication failed')

  todo = Todos(**req.model_dump(), owner_id=user.get('id'))

  db.add(todo)
  db.commit()


@router.put('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def update_todo(user: user_dependency, db: db_dependency, req: TodoRequest, todo_id: int=Path(gt=0)):
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details='Authentication failed')

  todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()

  if todo is None:
    raise HTTPException(status_code=404, detail='Todo not found')
  
  todo.title = req.title
  todo.description = req.description
  todo.priority = req.priority
  todo.complete = req.complete

  db.add(todo)
  db.commit()


@router.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_dependency, db: db_dependency, todo_id: int=Path(gt=0)):
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details='Authentication failed')

  todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id'))

  if todo is None:
    raise HTTPException(status_code=404, detail='Todo not found')
  
  todo.delete()
  db.commit()

