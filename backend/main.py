from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import desc
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


@app.post("/data/", response_model=schemas.Sensor)
def create_local_data(data: schemas.SensorCreate, db: Session = Depends(get_local_db)):
    """Endpoint para recibir datos del simulador interno o un microcontrolador."""
    db_item = models.SensorLocal(
        source_id=0,
        fecha=data.fecha,
        temperatura=data.temperatura,
        humedad=data.humedad,
        ph=data.ph,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/data/latest", response_model=schemas.Sensor)
def read_latest(
    db_local: Session = Depends(get_local_db),
    db_remote: Session = Depends(get_remote_db),
):
    """Get REAL-TIME latest data from REMOTE MySQL database, but check LOCAL for newer simulated data."""
    try:
        remote_data = crud.get_latest_remote_data(db_remote)
        local_data = (
            db_local.query(models.SensorLocal)
            .order_by(desc(models.SensorLocal.fecha))
            .first()
        )

        if remote_data and local_data:
            return local_data if local_data.fecha > remote_data.fecha else remote_data
        elif local_data:
            return local_data
        elif remote_data:
            return remote_data
        else:
            raise HTTPException(status_code=404, detail="No data available")
    except Exception as e:
        print(f"Remote DB Error: {e}")
        # If MySQL fails, try to fallback to Local DB
        local_data = (
            db_local.query(models.SensorLocal)
            .order_by(desc(models.SensorLocal.fecha))
            .first()
        )
        if local_data:
            return local_data
        raise HTTPException(status_code=503, detail="Database connection failed")


@app.get("/weather")
async def get_weather(lat: str, lon: str, api_key: str):
    """Proxy endpoint for External Weather (Meteostat) using user provided credentials."""
    data = await weather.get_external_weather(lat, lon, api_key)
    if not data:
        raise HTTPException(
            status_code=503, detail="External weather service unavailable"
        )
    return data
