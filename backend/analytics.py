from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import models


def get_last_minute_averages(db: Session):
    """Calculate average of T, H, pH for the last 60 seconds."""
    one_minute_ago = datetime.now() - timedelta(seconds=60)

    # Query local SQLite for speed
    records = (
        db.query(models.SensorLocal)
        .filter(models.SensorLocal.fecha >= one_minute_ago)
        .all()
    )

    if not records:
        return None

    avg_temp = sum(r.temperatura for r in records) / len(records)
    avg_hum = sum(r.humedad for r in records) / len(records)
    avg_ph = sum(r.ph for r in records) / len(records)

    return {
        "temperatura": round(avg_temp, 1),
        "humedad": round(avg_hum, 1),
        "ph": round(avg_ph, 2),
        "count": len(records),
    }
