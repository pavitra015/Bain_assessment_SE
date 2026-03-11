import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.services.config import settings
from backend.router import distance, history
from backend.models.database import create_tables

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

create_tables()

logger.info("Initializing FastAPI application")
app = FastAPI(
    title="Calculate distance API",
    description="API to use NominatimAPI to calculate distance between source and destination addresses",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

logger.info("Configuring CORS middleware")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

logger.info("Registering API routers")
app.include_router(distance.router)
app.include_router(history.router)
logger.info("Application setup complete")

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete - Ready to accept requests")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")

if __name__ == "__main__":
    logger.info("Starting FastAPI application on http://0.0.0.0:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)