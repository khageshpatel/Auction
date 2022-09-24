from fastapi import FastAPI, Request
from app.api.api_v1.api import api_router
import logging

app = FastAPI()

app.include_router(api_router)