from typing import Optional

from pydantic import BaseModel
from .product import Product
from app.common.types import AuctionStatus
from .user import User

# Auction Model
class Auction(BaseModel):
    auction_id: int
    product: Product
    auction_status: AuctionStatus
    start_time: int
    end_time: int
    number_extensions: int

    class Config:
        orm_mode = True

# Request to create auction
class AuctionCreateRequest(BaseModel):
    product_id: str
    user_id: int
    start_time: int
    min_bid: float

# Auction identifier
class AuctionId(BaseModel):
    auction_id: int
    user_id: int

# Request to place a bid.
class PlaceBidRequest(BaseModel):
    user_id: int
    bid: float
    auction_id: int

# Request to update auction status.
class UpdateAuctionStatusRequest(BaseModel):
    auction_id: int
    after_time: int
    from_status: AuctionStatus
    to_status: AuctionStatus