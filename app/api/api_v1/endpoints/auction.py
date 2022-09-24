from typing import Any, List
from app.schemas.auction import Auction, AuctionCreateRequest, AuctionId, PlaceBidRequest

from app.db.dependencies import get_auction_dal
from app.db.auction_dal import AuctionDal
from app.core.exception_handler import Handle
from fastapi import APIRouter, Depends, HTTPException

from app import schemas

router = APIRouter()


@router.post(
    "/create_auction",
    response_model = schemas.Auction)
async def create_auction(auction_create_request: AuctionCreateRequest, auction_dal: AuctionDal = Depends(get_auction_dal)) -> Auction:
    """
    Create auction.
    """
    try:
        return await auction_dal.create_auction(auction_create_request)
    except Exception as e:
        Handle(e)


@router.post(
    "/revoke_auction")
async def create_auction(request: AuctionId, auction_dal: AuctionDal = Depends(get_auction_dal)) -> None:
    """
    Revoke auction.
    """
    try:
        return await auction_dal.revoke_auction(request)
    except Exception as e:
        Handle(e)


@router.post(
    "/place_bid")
async def create_auction(request: PlaceBidRequest, auction_dal: AuctionDal = Depends(get_auction_dal)) -> None:
    """
    Place bid.
    """
    try:
        await auction_dal.place_bid(request)
    except Exception as e:
        Handle(e)