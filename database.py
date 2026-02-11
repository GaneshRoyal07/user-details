from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace with your actual database credentials
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost/test_db"
# If you don't have a password or using a different user/db, update the URL accordingly.
# Example: "mysql+pymysql://user:password@host/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
