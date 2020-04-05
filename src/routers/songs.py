from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import select
from database import engine
from database import concerts, concert_dirs, venues, songs, xref_concerts_concert_dir, xref_concerts_songs, xref_concerts_venues
from models.models import ConcertDirModel, ConcertModel, VenueModel, SetlistModel, SetlistSongModel, SongModel
from typing import List, Dict

router = APIRouter()
conn = engine.connect()


@router.get("/songs/", tags=['songs'])
async def all_songs():
    sql_query = select([songs])
    result = conn.execute(sql_query)
    json_result = jsonable_encoder([dict(row) for row in result])
    return json_result

# @router.get("/songs/{song_name}")
# async def get_concert(concert_date: str):
#     sql_query = select([concert_dirs]).where(concert_dirs.c.date_from_directory_name == concert_date)
#     result = conn.execute(sql_query)
#     json_result = jsonable_encoder([dict(row) for row in result])
#     return json_result

@router.post("/songs/", tags=['songs'])
async def post_songs(songs_list: List[SongModel]):
    json_songs_list = jsonable_encoder(songs_list)
    conn.execute(songs.insert(), json_songs_list)
    return json_songs_list

