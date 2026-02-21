from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SensorBase(BaseModel):
    fecha: datetime
    temperatura: float
    humedad: float
    ph: float


class SensorCreate(SensorBase):
    pass


class Sensor(SensorBase):
    id: int

    class Config:
        from_attributes = True
