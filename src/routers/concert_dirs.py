from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import select
from database import engine
from database import concerts, concert_dirs, venues, songs, xref_concerts_concert_dir, xref_concerts_songs, xref_concerts_venues
from models.models import ConcertDirModel, ConcertModel, VenueModel, SetlistModel, SetlistSongModel
from sqlalchemy.exc import IntegrityError
from loguru import logger


router = APIRouter()
conn = engine.connect()


# ConcertDir Entry Points
@router.get("/concert_dirs/", tags=['concert_dirs'])
async def all_concert_dirs():
    sql_query = select([concert_dirs])
    result = conn.execute(sql_query)
    return jsonable_encoder([dict(row) for row in result])

@router.get("/concert_dirs/{concert_date}", tags=['concert_dirs'])
async def get_concert(concert_date: str):
    sql_query = select([concert_dirs]).where(concert_dirs.c.date_from_directory_name == concert_date)
    result = conn.execute(sql_query)
    json_result = jsonable_encoder([dict(row) for row in result])
    return json_result

@router.post("/concert_dirs/", tags=['concert_dirs'])
async def post_concert_dir(concert_dir: ConcertDirModel):
    json_concert = jsonable_encoder(concert_dir)
    try:
        conn.execute(concert_dirs.insert(), json_concert)
    except IntegrityError as e:
        logger.info(f"Concert_dir already in the database: {e}")
    return concert_dir