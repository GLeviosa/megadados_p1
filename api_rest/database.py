from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker    
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("USER_SQL")
PASSWORD = os.getenv("PASSWORD_SQL")

engine = create_engine("mysql://"+USER+":"+PASSWORD+"@localhost/db_sql")

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)


