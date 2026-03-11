import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from backend.services.config import settings

logger = logging.getLogger(__name__)

logger.info(f"Initializing database connection: {settings.DATABASE_URL.split('://')[0]}://...")

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=5,
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        logger.debug("Database session created")
        yield db
    finally:
        db.close()
        logger.debug("Database session closed")


def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise