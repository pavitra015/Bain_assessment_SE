from typing import List, Optional, Dict
from datetime import  datetime
from pydantic import BaseModel

class DistanceRequest(BaseModel):
    source_address: str
    destination_address: str

class DistanceResponse(BaseModel):
    source_address: str
    destination_address: str
    distance_in_km: float
    distance_in_miles: float

class HistoryRequest(BaseModel):
    id: int
    source_address: str
    destination_address: str
    distance_km: float
    distance_miles: float
    created_at: datetime

    model_config = {"from_attributes": True}


class HistoryResponse(BaseModel):
    items: list[HistoryRequest]
    total: int