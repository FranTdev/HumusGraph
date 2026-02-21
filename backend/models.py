from sqlalchemy import Column, Integer, Float, DateTime, String, UniqueConstraint
from .database import Base


# Model for Remote MySQL Table (Existing)
class SensorMySQL(Base):
    __tablename__ = "sensores"

    id = Column(
        Integer, primary_key=True
    )  # Not observing unique constraint remotely, just PK for mapping
    fecha = Column(DateTime)
    temperatura = Column(Float)
    humedad = Column(Float)
    ph = Column(Float)


# Model for Local SQLite Table (New)
class SensorLocal(Base):
    __tablename__ = "sensor_local"

    id = Column(Integer, primary_key=True, index=True)  # Local Autoincrement ID
    source_id = Column(
        Integer, index=True
    )  # NOT UNIQUE because remote IDs are duplicated
    fecha = Column(
        DateTime, unique=True, index=True
    )  # Assume timestamp is unique per reading
    temperatura = Column(Float)
    humedad = Column(Float)
    ph = Column(Float)

    # Optional: Composite unique constraint if timestamp isn't strictly unique
    # __table_args__ = (UniqueConstraint('source_id', 'fecha', name='_source_fecha_uc'),)
