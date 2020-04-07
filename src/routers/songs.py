from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import select
from database import engine
from database import songs
from models.models import SongModel
from typing import List
from sqlalchemy.exc import IntegrityError
from loguru import logger

router = APIRouter()
conn = engine.connect()


@router.get("/songs/", tags=['songs'])
async def all_songs():
    sql_query = select([songs])
    result = conn.execute(sql_query)
    json_result = jsonable_encoder([dict(row) for row in result])
    return json_result

@router.post("/songs/", tags=['songs'])
async def post_songs(songs_list: List[SongModel]):
    json_songs_list = jsonable_encoder(songs_list)
    for song in json_songs_list:
        try:
            conn.execute(songs.insert(), song)
        except IntegrityError as e:
            logger.info(f"Song already in the database: {e}")
    return json_songs_list

