from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Song(Base):
  __tablename__ = "songs"
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  artist = Column(String)
  album = Column(String)
  url = Column(String) # demo audio url or placeholder