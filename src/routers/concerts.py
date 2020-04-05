from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import select
from database import engine
from database import concerts, concert_dirs, venues, songs, xref_concerts_concert_dir, xref_concerts_songs, xref_concerts_venues
from models.models import ConcertDirModel, ConcertModel, VenueModel, SetlistModel, SetlistSongModel

router = APIRouter()
conn = engine.connect()


@router.get("/concerts/", tags=['concerts'])
async def all_concerts():
    sql_query = select([concerts])
    result = conn.execute(sql_query)
    return jsonable_encoder([dict(row) for row in result])


@router.post("/concerts/", tags=['concerts']) #Create a concert TODO: Should I support put and post?
async def post_concert(concert: ConcertModel):
    json_concert = jsonable_encoder(concert)
    conn.execute(concerts.insert(), json_concert)
    return concert


@router.get("/concerts/{concert_date}", tags=['concerts'])
async def get_concert(concert_date: str):
    sql_query = select([concerts]).where(concerts.c.date == concert_date)
    result = conn.execute(sql_query)
    json_result = jsonable_encoder([dict(row) for row in result])
    return json_result


@router.delete("/concerts/{concert_date}", tags=['concerts'])
async def del_concert(concert_date: str):
    get_concert_id_query = select([concerts]).where(concerts.c.date == concert_date)
    result = conn.execute(get_concert_id_query).fetchone()
    concert_id = result["id"]
    conn.execute(concerts.delete().where(concerts.c.id == concert_id))
    return {"result": f"Deleted concert{concert_date}"}
