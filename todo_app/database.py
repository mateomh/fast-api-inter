from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ! SQL LITE CONFIG
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# engine = create_engine(
#   SQLALCHEMY_DATABASE_URL,
#   connect_args={
#     "check_same_thread": False,
#   }
# )


# ! POSTGRES CONFIG
# SQLALCHEMY_DATABASE_URL = 'postgresql://root:password@pgdb:5432/todosappdb'

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


# ! MYSQL CONFIG
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:password@mysqldb:3306/todosappdb'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()