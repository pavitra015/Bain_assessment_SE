import logging
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from backend.models.database import get_db
from backend.models.history import History

from backend.schema import DistanceRequest, DistanceResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/distance", response_model=None)
def get_distance(
        request: DistanceRequest,
        response: Response,
        db: Session = Depends(get_db),
):
    logger.info(f"Received distance calculation request - Source: '{request.source_address}', Destination: '{request.destination_address}'")
    
    locator = Nominatim(user_agent="distance")
    try:
        logger.debug(f"Geocoding source address: '{request.source_address}'")
        source_location = locator.geocode(request.source_address, timeout=10)
        
        logger.debug(f"Geocoding destination address: '{request.destination_address}'")
        destination_location = locator.geocode(request.destination_address, timeout=10)
    except GeocoderTimedOut as e:
        logger.error(f"Geocoding timeout error: {str(e)}")
        raise HTTPException(
            status_code=408,
            detail=f"Unable to process your request: {str(e)}. Please check and try again.",
        )

    if source_location is None:
        logger.warning(f"Could not resolve source address: '{request.source_address}'")
        raise HTTPException(
            status_code=422,
            detail=f"Could not resolve destination address: '{request.source_address}'. Please check and try again.",
        )

    if destination_location is None:
        logger.warning(f"Could not resolve destination address: '{request.destination_address}'")
        raise HTTPException(
            status_code=422,
            detail=f"Could not resolve destination address: '{request.destination_address}'. Please check and try again.",
        )

    source_coords = (source_location.latitude, source_location.longitude)
    destination_coords = (destination_location.latitude, destination_location.longitude)
    
    logger.debug(f"Source coordinates: {source_coords}")
    logger.debug(f"Destination coordinates: {destination_coords}")

    # Calculate the distance
    distance_in_kms = geodesic(source_coords, destination_coords).km
    distance_in_miles = geodesic(source_coords, destination_coords).miles

    logger.info(f"Distance calculated: {distance_in_kms:.2f} km ({distance_in_miles:.2f} miles) from '{request.source_address}' to '{request.destination_address}'")

    # Save to database
    try:
        history = History(
            source_address=request.source_address,
            destination_address=request.destination_address,
            distance_in_kms=distance_in_kms,
            distance_in_miles=distance_in_miles,
            created_at=datetime.now(),
        )

        db.add(history)
        db.commit()
        db.refresh(history)
        logger.info(f"Distance calculation saved to database with ID: {history.id}")
    except Exception as e:
        logger.error(f"Failed to save distance calculation to database: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to save calculation to database"
        )

    return {
        "id": history.id,
        "source_address": history.source_address,
        "destination_address": history.destination_address,
        "distance_in_miles": history.distance_in_miles,
        "distance_in_kms": history.distance_in_kms,
        "created_at": history.created_at.isoformat() if history.created_at else None
    }