from fastapi import FastAPI, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependency = Annotated[Session,Depends(get_db)]

class TodoRequest(BaseModel):
  title: str = Field(min_length=3)
  description: str = Field(min_length=3, max_length=100)
  priority: int = Field(gt=0, lt=6)
  complete: bool

@app.get('/health-check')
def root_path():
  return { "status": "ok" }

@app.get('/todos', status_code=status.HTTP_200_OK)
def read_all(db: db_dependency):
  return db.query(Todos).all()

@app.get('/todos/{todo_id}', status_code=status.HTTP_200_OK)
def get_single_todo(db: db_dependency, todo_id: int = Path(gt=0)):
  print(f"TODOS ID: {todo_id}")
  todo = db.query(Todos).filter(Todos.id == todo_id).first()

  if todo is not None:
    return todo
    
  raise HTTPException(status_code=404, detail='Todo not found')

@app.post('/todos', status_code=status.HTTP_201_CREATED)
def create_todo(db: db_dependency, req: TodoRequest):
  todo = Todos(**req.model_dump())

  db.add(todo)
  db.commit()

@app.put('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db: db_dependency, req: TodoRequest, todo_id: int=Path(gt=0)):
  todo = db.query(Todos).filter(Todos.id == todo_id).first()

  if todo is None:
    raise HTTPException(status_code=404, detail='Todo not found')
  
  todo.title = req.title
  todo.description = req.description
  todo.priority = req.priority
  todo.complete = req.complete

  db.add(todo)
  db.commit()

@app.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: db_dependency, todo_id: int=Path(gt=0)):
  todo = db.query(Todos).filter(Todos.id == todo_id)

  if todo is None:
    raise HTTPException(status_code=404, detail='Todo not found')
  
  todo.delete()
  db.commit()