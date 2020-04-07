from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import select
from database import engine
from database import venues
from models.models import VenueModel
from typing import List
from sqlalchemy.exc import IntegrityError
from loguru import logger

router = APIRouter()
conn = engine.connect()


@router.get("/venues/", tags=['venues'])
async def get_venue_route():
    sql_query = select([venues])
    result = conn.execute(sql_query)
    return jsonable_encoder([dict(row) for row in result])


@router.get("/venues/{name}", tags=['venues'])
async def get_venue_by_name(name: str):
    sql_query = select([venues]).where(venues.c.name == name)
    result = conn.execute(sql_query)
    json_result = jsonable_encoder([dict(row) for row in result])
    return json_result


@router.post("/venues/get_id/", tags=['venues'])
async def get_venue_id(venue: VenueModel):
    json_venue = jsonable_encoder(venue)
    venue_results = conn.execute(select([venues]).where(venues.c.name == json_venue['name'])
                                 .where(venues.c.city == json_venue['city'])
                                 .where(venues.c.state == json_venue['state'])).fetchall()
    if len(venue_results) == 1:
        return venue_results[0]['id']
    elif len(venue_results) > 1:
        return "Found more than one."
    else:
        return "Could not find venue"


@router.post("/venues/", tags=['venues'])
async def post_venue(venue: List[VenueModel]):
    json_venue_list = jsonable_encoder(venue)

    for json_venue in json_venue_list:
        # Check to see if venue name is already in the database
        venue_name_results = conn.execute(select([venues]).where(venues.c.name == json_venue['name'])).fetchall()
        if len(venue_name_results) == 0:
            try:
                conn.execute(venues.insert(), json_venue)
            except IntegrityError as e:
                logger.info(f"Venue Data already in the database: {e}")
            continue

        # Check to see if venue Name and City are already in the database
        venue_name_city_results = conn.execute(select([venues]).where(venues.c.name == json_venue['name']).where(venues.c.city == json_venue['city'])).fetchall()
        if len(venue_name_city_results) == 0:
            try:
                conn.execute(venues.insert(), json_venue)
            except IntegrityError as e:
                logger.info(f"Venue Data already in the database: {e}")

            continue

        # Check to see if venue Name and City and State are already in the database
        venue_name_city_state_results = conn.execute(select([venues]).where(venues.c.name == json_venue['name']).where(venues.c.city == json_venue['city']).where(venues.c.state == json_venue['state'])).fetchall()
        if len(venue_name_city_state_results) == 0:
            try:
                conn.execute(venues.insert(), json_venue)
            except IntegrityError as e:
                logger.info(f"Venue Data already in the database: {e}")
            continue

    return json_venue_list