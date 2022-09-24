from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.connector import Base
from sqlalchemy.orm import relationship

# User table
class Product(Base):
    __tablename__ = "Product"

    product_id = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("User.user_id"))
    user = relationship("User", back_populates="product")

    auctions = relationship("Auction", back_populates="product")