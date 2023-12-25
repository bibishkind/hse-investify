# db.py
import dotenv
from sqlalchemy import create_engine
from config.config import DATABASE_URL
import logging
from sqlalchemy.orm import sessionmaker
from models.models import Base

dotenv.load_dotenv()
engine = create_engine(DATABASE_URL)

logging.info("db connect")

SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)
db = SessionLocal()
