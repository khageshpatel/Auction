from itertools import product
from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.connector import Base
from sqlalchemy.orm import relationship

# User table
class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    product = relationship("Product", back_populates="user")
    auction = relationship("Auction", back_populates="user")
    bids = relationship("AuctionBid", back_populates="user")