from sqlalchemy import Column, Integer, String
from app.db.connector import Base

# User table
class User(Base):
    __tablename__ = "User"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=True)