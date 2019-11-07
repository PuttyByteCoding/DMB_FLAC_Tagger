from pydantic import BaseModel

class PydanticSongModel(BaseModel):
    id: int
    name: str