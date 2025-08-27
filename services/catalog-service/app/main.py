import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from .models import Base, Song
from .schemas import SongOut


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./catalog.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)


# seed a few songs if empty
with SessionLocal() as db:
 if db.query(Song).count() == 0:
  db.add_all([
  Song(title="Lost Stars", artist="Adam Levine", album="Begin Again", url="/media/lost-stars.mp3"),
  Song(title="Nand", artist="Instrumental", album="Lo-Fi", url="/media/nand.mp3"),
  Song(title="Sky High", artist="Alex", album="EDM", url="/media/sky-high.mp3"),
  ])
  db.commit()


app = FastAPI(title="Catalog Service")


@app.get("/songs", response_model=list[SongOut])
def list_songs():
 with SessionLocal() as db:
  songs = db.query(Song).all()
  return songs


@app.get("/catalog/health")
def health():
 return {"status": "ok"}