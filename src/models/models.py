from pydantic import BaseModel
from typing import List, Dict


class VenueModel(BaseModel):
    name: str
    city: str
    state: str
    country: str


class ConcertModel(BaseModel):
    date: str
    band_configuration: str
    venue_name: str  #TODO: Create a separate tabl and model for this?
    venue_city: str
    venue_state: str
    venue_country: str
    taper_name: str #TODO: Create a separate tabl and model for this?
    recording_type: str #TODO: Create a separate tabl and model for this?
    description: str


class ConcertDirModel(BaseModel):
    local_path: str
    web_path: str
    date_from_directory_name: str
    band_configuration_from_directory_name: str

class SongModel(BaseModel):
    name: str


class SetlistSongModel(BaseModel):
    position: int
    song_title: str


class SetlistModel(BaseModel):
    concert_date: str
    setlist: List[SetlistSongModel]