from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import asyncio
from contextlib import asynccontextmanager

from . import crud, models, schemas, sync, database, weather

models.Base.metadata.create_all(bind=database.engine_sqlite)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background sync task
    asyncio.create_task(sync.sync_worker())
    yield


app = FastAPI(lifespan=lifespan)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get LOCAL DB session
def get_local_db():
    db = database.SessionSQLite()
    try:
        yield db
    finally:
        db.close()


# Dependency to get REMOTE DB session
def get_remote_db():
    db = database.SessionMySQL()
    try:
        yield db
    finally:
        db.close()


@app.get("/data/", response_model=List[schemas.Sensor])
def read_history(skip: int = 0, limit: int = 50, db: Session = Depends(get_local_db)):
    """Get historical data from LOCAL SQLite database (for graphs/table)."""
    data = crud.get_local_history(db, skip=skip, limit=limit)
    return data


@app.get("/data/latest", response_model=schemas.Sensor)
def read_latest(db: Session = Depends(get_remote_db)):
    """Get REAL-TIME latest data from REMOTE MySQL database."""
    try:
        data = crud.get_latest_remote_data(db)
        if data is None:
            raise HTTPException(status_code=404, detail="No data available")
        return data
    except Exception as e:
        print(f"Connection Error: {e}")
        # If MySQL fails, we return 503 so frontend knows to pause/alert
        raise HTTPException(status_code=503, detail="Database connection failed")


@app.get("/weather")
async def get_weather():
    """Proxy endpoint for External Weather (Meteostat)."""
    data = await weather.get_external_weather()
    if not data:
        raise HTTPException(
            status_code=503, detail="External weather service unavailable"
        )
    return data
