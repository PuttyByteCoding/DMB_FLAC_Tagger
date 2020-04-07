from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import select
from database import engine
from database import tapers
from models.models import TaperModel
from typing import List
from sqlalchemy.exc import IntegrityError
from loguru import logger

router = APIRouter()
conn = engine.connect()


@router.get("/tapers/", tags=['tapers'])
async def all_tapers():
    sql_query = select([tapers])
    result = conn.execute(sql_query)
    json_result = jsonable_encoder([dict(row) for row in result])
    return json_result


@router.post("/tapers/", tags=['tapers'])
async def post_taper(taper_list: List[TaperModel]):
    json_tapers_list = jsonable_encoder(taper_list)
    for taper in json_tapers_list:
        try:
            conn.execute(tapers.insert(), taper)
        except IntegrityError as e:
            logger.info(f"Taper Data already in the database: {e}")
    return json_tapers_list

