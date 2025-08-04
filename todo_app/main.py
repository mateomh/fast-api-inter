from fastapi import FastAPI, Depends, HTTPException, Path, status
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
