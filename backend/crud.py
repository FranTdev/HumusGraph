from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from datetime import datetime
from . import models


# --- Remote Operations ---
def get_latest_remote_data(db: Session):
    return db.query(models.SensorMySQL).order_by(desc(models.SensorMySQL.fecha)).first()


def get_new_remote_records_by_date(db: Session, last_synced_date: datetime):
    """Fetch records strictly newer than the last timestamp we have."""
    return (
        db.query(models.SensorMySQL)
        .filter(models.SensorMySQL.fecha > last_synced_date)
        .order_by(models.SensorMySQL.fecha.asc())
        .limit(100)
        .all()
    )


def get_remote_records_batch(db: Session, limit: int = 100):
    """Fetch the latest records by DATE to bootstrap."""
    records = (
        db.query(models.SensorMySQL)
        .order_by(desc(models.SensorMySQL.fecha))
        .limit(limit)
        .all()
    )
    # Return sorted ascending by date
    return sorted(records, key=lambda x: x.fecha)


# --- Local Operations ---
def get_local_history(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.SensorLocal)
        .order_by(desc(models.SensorLocal.fecha))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_last_synced_date(db: Session):
    """Get the latest timestamp we have stored locally."""
    last_record = (
        db.query(models.SensorLocal).order_by(desc(models.SensorLocal.fecha)).first()
    )
    return last_record.fecha if last_record else None


def create_local_record(db: Session, remote_record: models.SensorMySQL):
    # Check if exists by FECHA (timestamp)
    exists = db.query(models.SensorLocal).filter_by(fecha=remote_record.fecha).first()
    if not exists:
        local_data = models.SensorLocal(
            source_id=remote_record.id,
            fecha=remote_record.fecha,
            temperatura=remote_record.temperatura,
            humedad=remote_record.humedad,
            ph=remote_record.ph,
        )
        db.add(local_data)
        db.commit()
        db.refresh(local_data)
        return local_data
    return None
