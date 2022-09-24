from typing import Any, List
from app.schemas.auction import Auction, AuctionCreateRequest, AuctionId, PlaceBidRequest, UpdateAuctionStatusRequest

from app.db.dependencies import get_auction_dal
from app.db.auction_dal import AuctionDal
from app.core.exception_handler import Handle
from fastapi import APIRouter, Depends, HTTPException
from app.common.types import AuctionStatus
from app.core.celery_worker import create_task
from app import schemas
import time 

router = APIRouter()


@router.post(
    "/create_auction",
    response_model = schemas.Auction)
async def create_auction(auction_create_request: AuctionCreateRequest, auction_dal: AuctionDal = Depends(get_auction_dal)) -> Auction:
    """
    Create auction.
    """
    try:
        auction =  await auction_dal.create_auction(auction_create_request)
        epoch_time = int(time.time())
        
        # Create two background tasks to update the auction status.
        create_task.s(auction.auction_id, auction.start_time, "WAITING", "ACTIVE").apply_async(countdown=(auction.start_time - epoch_time))
        create_task.s(auction.auction_id, auction.end_time, "ACTIVE", "STOPPED").apply_async(countdown=(auction.end_time - epoch_time))
        return auction
    except Exception as e:
        Handle(e)


@router.post(
    "/revoke_auction")
async def revoke_auction(request: AuctionId, auction_dal: AuctionDal = Depends(get_auction_dal)) -> None:
    """
    Revoke auction.
    """
    try:
        return await auction_dal.revoke_auction(request)
    except Exception as e:
        Handle(e)


@router.post(
    "/place_bid")
async def place_bid(request: PlaceBidRequest, auction_dal: AuctionDal = Depends(get_auction_dal)) -> None:
    """
    Place bid.
    """
    try:
        await auction_dal.place_bid(request)
    except Exception as e:
        Handle(e)

@router.post(
    "/update_auction_status")
async def update_auction_status(request: UpdateAuctionStatusRequest, auction_dal: AuctionDal = Depends(get_auction_dal)) -> None:
    """
    Place bid.
    """
    try:
        more_wait =  await auction_dal.update_status(request.auction_id, request.after_time, request.from_status, request.to_status)
        if more_wait != 0:
            # We couldn't update the db we must try after some time.
            create_task.s(request.auction_id, request.after_time, request.from_status, request.to_status).apply_async(countdown=more_wait)
    except Exception as e:
        Handle(e)