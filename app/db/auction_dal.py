from msilib.schema import Error
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.product import Product
from app import schemas
from app.models.auction import Auction, AuctionBid
from app.common.types import AuctionStatus
from app.core.config import settings
from app.common.constants import ErrorCode
from fastapi import HTTPException
from sqlalchemy.future import select
import logging
import time

# Auction data access layer.
class AuctionDal():
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    async def create_auction(self, request: schemas.AuctionCreateRequest) -> Auction:
        # Creates an auction.
        auction = Auction(
            product_id = request.product_id,
            user_id = request.user_id,
            auction_status = AuctionStatus.WAITING,
            start_time = request.start_time,
            end_time = request.start_time + settings.AUCTION_DURATION_SECS,
            number_extensions = 0,
            min_bid = request.min_bid
            )
        self.db_session.add(auction)
        await self.db_session.flush()
        await self.db_session.refresh(auction)
        return auction
    
    async def revoke_auction(self, request : schemas.AuctionId) -> None:
        # Revokes an auction as well as performs sanitation checks.
        auction = await self.db_session.get(Auction, request.auction_id)
        if auction is None:
            raise HTTPException(status_code=ErrorCode.NOT_PRESNT, detail="Auction does not exist")
        if auction.user_id != request.user_id:
            raise HTTPException(status_code=ErrorCode.NOT_AUTHORISED, detail="Don't have permission to modify this")
        if auction.auction_status == AuctionStatus.STOPPED:
            raise HTTPException(status_code=ErrorCode.NOT_AUTHORISED, detail="Can't revoke finished auction")
        auction.auction_status = AuctionStatus.REVOKED
        await self.db_session.flush()
    
    async def place_bid(self, request: schemas.PlaceBidRequest) -> None:
        # Places a bid.
        auction = await self.db_session.get(Auction, request.auction_id)
        if auction is None:
            raise HTTPException(status_code=ErrorCode.NOT_PRESNT, detail="Auction does not exist")
        if auction.auction_status != AuctionStatus.ACTIVE:
            raise HTTPException(status_code=ErrorCode.NOT_PRESNT, detail="Auction is not active")
        
        # Note that this does not fetch all rows.
        bids = await self.db_session.execute(select(AuctionBid).filter(AuctionBid.auction_id == request.auction_id).order_by(AuctionBid.bid))
        top_bid = bids.scalars().first()
        if top_bid is None:
            if request.bid <= auction.min_bid:
                raise HTTPException(status_code=ErrorCode.INVLID_OPERATION, detail="Provided bid less than min bid")
            bid  = AuctionBid(auction_id = request.auction_id, bid = request.bid, user_id = request.user_id)
            self.db_session.add(bid)
            self.db_session.flush()
            return
        if top_bid.user_id == request.user_id:
            raise HTTPException(status_code=ErrorCode.INVLID_OPERATION, detail="User can't place another top bid")
        if top_bid.bid * ( 1 + settings.MIN_AUCTION_DELTA_PCT / 100.0) >= request.bid:
            raise HTTPException(status_code=ErrorCode.INVLID_OPERATION, detail="New bid must outmatch existing bid by " + str(settings.MIN_AUCTION_DELTA_PCT) + '%')
        bid  = AuctionBid(auction_id = request.auction_id, bid = request.bid, user_id = request.user_id)
        self.db_session.add(bid)
        epoch_time = int(time.time())
        time_left =  auction.end_time - epoch_time

        # This is just for safety we will be marking auction invalid in separate pubsub queue.
        if time_left <= 0:
            raise HTTPException(status_code=ErrorCode.INVLID_OPERATION, detail="Auction has ended")
        
        if time_left <= settings.AUCTION_END_WINDOW_SEC and auction.number_extensions < settings.AUCTION_MAX_EXTEND_TIMES:
            auction.number_extensions = auction.number_extensions + 1
            auction.end_time  += settings.AUCTION_EXTEND_WINDOW_SEC

        self.db_session.flush()
    
    async def update_status(self, auction_id: int, after_time: int, from_status: AuctionStatus, to_status: AuctionStatus) -> int:
        # Update auction status
        # Returns amount of time after which this should be retried
        auction = await self.db_session.get(Auction, auction_id)
        if auction.auction_status != from_status:
            # DB has changed state
            return 0
        epoch_time = int(time.time())
        if epoch_time < after_time:
            # This should not hapend unless true time between server is widely different.
            return after_time - epoch_time

        ref_time = auction.start_time if from_status == AuctionStatus.WAITING else auction.end_time
        if ref_time <= epoch_time:
            # change status
            auction.auction_status = to_status
            self.db_session.flush()
            return 0
        
        # Maybe end time has been increased we should retry this op
        return auction.start_time - epoch_time