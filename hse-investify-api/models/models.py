# models.py
from sqlalchemy import MetaData, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base()

class Notification(Base):
    __tablename__ = "notifications"
    metadata = metadata
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    ticker = Column(String, nullable=False)
    indicator_name = Column(String, nullable=False)
    initial_indicator_value = Column(Float, nullable=False)
    expected_indicator_value = Column(Float, nullable=False)
    active = Column(Boolean, default=False, nullable=False)
