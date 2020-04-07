from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import select, text
from database import engine
from database import concerts, concert_dirs, venues, songs, xref_concerts_concert_dir, xref_concerts_songs, xref_concerts_venues
from models.models import ConcertDirModel, ConcertModel, VenueModel, SetlistModel, SetlistSongModel
from sqlalchemy.exc import IntegrityError
from loguru import logger

router = APIRouter()
conn = engine.connect()


@router.post("/setlists/", tags=['setlists']) #Create a setlist TODO: Should I support put and post?
async def post_setlist(setlist: SetlistModel):
    #TODO: Handle a concert date that does not exist
    concert_date = setlist.concert_date
    sql_get_concert_query = select([concerts]).where(concerts.c.date == concert_date)
    result = conn.execute(sql_get_concert_query).fetchone()
    concert_id = result["id"]

    for song in setlist.setlist:
        sql_get_song_id_query = select([songs]).where(songs.c.name == song.song_title)
        result = conn.execute(sql_get_song_id_query).fetchone()
        song_id = result["id"]
        try:
            conn.execute(xref_concerts_songs.insert(),
                         {
                             'concert_id': concert_id,
                             'song_id': song_id,
                             'setlist_position': song.position
                         })
        except IntegrityError as e:
            logger.info(f"Setlist already in the database: {e}")
    return {"message": "Setlist Added"}


@router.put("/setlists/", tags=['setlists']) #Update a setlist TODO: Should I support put and post?
async def put_setlist(setlist: SetlistModel):
    # TODO: Handle a concert date that does not exist
    concert_date = setlist.concert_date
    sql_get_concert_query = select([concerts]).where(concerts.c.date == concert_date)
    result = conn.execute(sql_get_concert_query).fetchone()
    concert_id = result["id"]

    for song in setlist.setlist:
        sql_get_song_id_query = select([songs]).where(songs.c.name == song.song_title)
        result = conn.execute(sql_get_song_id_query).fetchone()
        song_id = result["id"]
        try:
            conn.execute(xref_concerts_songs.insert(),
                         {
                             'concert_id': concert_id,
                             'song_id': song_id,
                             'setlist_position': song.position
                         })
        except IntegrityError as e:
            logger.info(f"Setlist already in the database: {e}")

    return {"message": "Setlist Added"}


@router.get("/setlists/{concert_date}", tags=['setlists'])
async def get_concert_setlist(concert_date: str):
    # TODO: Handle a concert date that does not exist
    sql_get_concert_query = select([concerts]).where(concerts.c.date == concert_date)
    result = conn.execute(sql_get_concert_query).fetchone()
    concert_id = result["id"] #TODO: Why doesn't this work?  I can pass "1" below, and it works.  why doens't my cast work?
    setlist_query = text(
        "SELECT setlist.setlist_position, songs.name FROM (SELECT * FROM xref_concerts_songs WHERE xref_concerts_songs.concert_id = :c) as setlist LEFT JOIN songs on setlist.song_id = songs.id")
    result = conn.execute(setlist_query, c=concert_id)
    json_result = jsonable_encoder([dict(row) for row in result])
    return json_result