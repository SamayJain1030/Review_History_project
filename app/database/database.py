

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.base import Base  # Import Base
  # Import Blog after Base is defined as it is necessary for SqlAlchemy to register the model during the call to create_all(bind = engine)

psql_db_url = "postgresql://user:password@host:port/dbname"

engine = create_engine(psql_db_url)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()