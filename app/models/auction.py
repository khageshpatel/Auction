from itertools import product
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float
from app.db.connector import Base
from sqlalchemy.orm import relationship
from  app.common.types import AuctionStatus

# Auction table
class Auction(Base):
    __tablename__ = "Auction"

    auction_id = Column(Integer, primary_key=True, index=True)
    
    product = relationship("Product", back_populates="auctions", lazy="joined")
    product_id = Column(String, ForeignKey("Product.product_id"))

    user_id = Column(Integer, ForeignKey("User.user_id"))
    user = relationship("User", back_populates="auction")

    auction_status = Column(Enum(AuctionStatus))

    start_time = Column(Integer)
    end_time = Column(Integer)

    number_extensions = Column(Integer)

    min_bid = Column(Float)
    bids = relationship("AuctionBid", back_populates="auction")

class AuctionBid(Base):
    __tablename__ = "AuctionBid"

    bid_id = Column(Integer, primary_key=True, index=True)

    auction_id = Column(Integer, ForeignKey("Auction.auction_id"))
    auction = relationship("Auction", back_populates="bids")

    bid = Column(Float)
    user_id = Column(Integer, ForeignKey("User.user_id"))
    user = relationship("User", back_populates="bids")
