from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import select
from database import engine
from database import guests
from models.models import GuestModel
from typing import List
from sqlalchemy.exc import IntegrityError
from loguru import logger

router = APIRouter()
conn = engine.connect()


@router.get("/guests/", tags=['guests'])
async def all_guests():
    sql_query = select([guests])
    result = conn.execute(sql_query)
    json_result = jsonable_encoder([dict(row) for row in result])
    return json_result

@router.get("/guests/{guest_name}", tags=['guests'])
async def get_guest(guest_name: str):
    sql_query = select([guests]).where(guests.c.name == guest_name)
    result = conn.execute(sql_query)
    json_result = jsonable_encoder([dict(row) for row in result])
    return json_result

@router.post("/guests/", tags=['guests'])
async def post_guests(guest: List[GuestModel]):
    json_guest_list = jsonable_encoder(guest)
    for guest in json_guest_list:
        try:
            conn.execute(guests.insert(), guest)
        except IntegrityError as e:
            logger.info(f"Guest Data already in the database: {e}")
    return json_guest_list

