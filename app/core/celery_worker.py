from app.schemas import auction
from celery import Celery
from app.core.config import settings
from app.common.types import AuctionStatus
from app.db.connector import async_session, sync_session
from app.db.auction_dal import AuctionDal
from asgiref.sync import async_to_sync
import asyncio
import requests

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

def send_internal_request(auction_id: int, after_time: int, from_status: AuctionStatus, to_status: AuctionStatus):
    json_data = {
        'auction_id': auction_id,
        'after_time': after_time,
        'from_status': str(from_status),
        'to_status': str(to_status),
    }
    requests.post('http://localhost:8000/auction/update_auction_status', json=json_data)

@celery.task(name="change_auction_status")
def create_task(auction_id: int, after_time: int, from_status: AuctionStatus, to_status: AuctionStatus):
    # Sadly celery does not work very well with async so we will making it sync. Its fine as this is background job.
    #
    # Honestly this is bit of a hack we are making internal server call to execute async jobs as celery has problem executing them.
    send_internal_request(auction_id, after_time, from_status, to_status)