# catalog-service/app/seed_data.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, Song

# Database URL (using SQLite for local; can switch to Postgres in K8s)
DATABASE_URL = "sqlite:///./catalog.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Create tables
Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()
    try:
        # Clear old data
        db.query(Song).delete()

        # Add sample Spotify-like catalog (songs + artists + albums)
        songs = [
            Song(
                title="Shape of You",
                artist="Ed Sheeran",
                album="Divide",
                duration=233,
                genre="Pop"
            ),
            Song(
                title="Blinding Lights",
                artist="The Weeknd",
                album="After Hours",
                duration=200,
                genre="Synthwave"
            ),
            Song(
                title="Levitating",
                artist="Dua Lipa",
                album="Future Nostalgia",
                duration=203,
                genre="Pop"
            ),
            Song(
                title="Numb",
                artist="Linkin Park",
                album="Meteora",
                duration=185,
                genre="Rock"
            ),
            Song(
                title="Rolling in the Deep",
                artist="Adele",
                album="21",
                duration=228,
                genre="Soul"
            ),
        ]

        db.add_all(songs)
        db.commit()
        print("✅ Database seeded successfully with Spotify-like songs!")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
