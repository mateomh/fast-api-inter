from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from database import Base


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@pgdb:5432/test_todosappdb'

engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()


def override_get_current_user():
  return {"username": "testinguser", "id": 1, "user_role": "admin"}

