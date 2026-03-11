from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func

from backend.models.database import Base


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    source_address = Column(String, index=True)
    destination_address = Column(String, index=True)
    distance_in_miles = Column(Float, index=True)
    distance_in_kms = Column(Float, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())