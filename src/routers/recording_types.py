from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import select
from database import engine
from database import recording_types
from models.models import RecordingTypeModel
from typing import List
from sqlalchemy.exc import IntegrityError
from loguru import logger

router = APIRouter()
conn = engine.connect()


@router.get("/recording_types/", tags=['Recording Types'])
async def all_recording_types():
    sql_query = select([recording_types])
    result = conn.execute(sql_query)
    json_result = jsonable_encoder([dict(row) for row in result])
    return json_result


@router.post("/recording_types/", tags=['Recording Types'])
async def post_recording_types(taper_list: List[RecordingTypeModel]):
    json_recording_types_list = jsonable_encoder(taper_list)
    for recording_type in json_recording_types_list:
        try:
            conn.execute(recording_types.insert(), recording_type)
        except IntegrityError as e:
            logger.info(f"Recording Type already in the database: {e}")
    return json_recording_types_list

