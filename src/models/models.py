from pydantic import BaseModel
from typing import List, Dict


class TaperModel(BaseModel):
    name: str


class RecordingTypeModel(BaseModel):
    rec_type: str


class VenueModel(BaseModel):
    name: str
    city: str
    state: str
    # country: str


class ConcertModel(BaseModel):
    date: str
    band_configuration: str
    venue_id: int
    taper_name: str #TODO: Create a separate tabl and model for this?
    recording_type: str #TODO: Create a separate tabl and model for this?
    notes: str
    info_text_file_contents: str


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


class GuestModel(BaseModel):
    name: str
    instrument: str
