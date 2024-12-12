# 001 start

# 'pip install SQLAlchemy' first
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# if we are using sqlite:
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# if we are using postgresql:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# if we are using sqlite, we will need to include connect_args as we did below, if we were using postgres, we wont need to include connect_args
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# when we call this 'SessionLocal', that actual instance of the class(SessionLocal) will be a database session

Base = declarative_base()
# we will import this Base into our models.py file, this is what will allow the database to update.

# 001 end
