# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os

# # Replace with your actual database URL
# DATABASE_URL = os.getenv("DATABASE_URL","postgresql://postgres:12345678@127.0.0.1:5432/energy_management")
# # postgresql://postgres:12345678@127.0.0.1:5432/energy_management


# # SQLAlchemy engine
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# # SessionLocal instance for database session
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base class for the ORM models
# Base = declarative_base()


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:12345678@localhost/energy_management'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,connect_args={},future=True
)

SessionLocal = sessionmaker(
    autocommit=False,autoflush=False,bind=engine,future=True
)

Base = declarative_base()

# DB Utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()