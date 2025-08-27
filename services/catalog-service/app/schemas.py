from pydantic import BaseModel


class SongOut(BaseModel):
 id: int
 title: str
 artist: str
 album: str
 url: str


class Config:
 from_attributes = True