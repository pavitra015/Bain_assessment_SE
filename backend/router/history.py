import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from backend.models.database import get_db
from backend.models.history import History

from backend.schema import HistoryRequest, HistoryResponse

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    logger.info("Received request to fetch distance calculation history")
    
    try:
        history = db.query(History).order_by(History.created_at.desc()).all()
        
        if not history:
            logger.warning("No history records found in database")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No history found")
        
        logger.info(f"Successfully retrieved {len(history)} history records")
        
        return [
            {
                "id": item.id,
                "source_address": item.source_address,
                "destination_address": item.destination_address,
                "distance_in_miles": item.distance_in_miles,
                "distance_in_kms": item.distance_in_kms,
                "created_at": item.created_at.isoformat() if item.created_at else None
            }
            for item in history
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving history from database: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve history"
        )