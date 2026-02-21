from sqlalchemy import Column, Integer, Float, DateTime, String
from database import Base
import datetime


class SensorData(Base):
    __tablename__ = "datos"  # Assuming table name is 'datos', user just said "La tabla: id, fecha..." but didn't name it. I'll guess or verify.
    # Wait, looking at user prompt: "database='vermicompost'". "La tabla: id, fecha...". No specific table name given. Let me check or default to 'sensor_data' or 'mediciones'.
    # A safe bet is checking if the table exists or just creating one if I have permissions. But here I am connecting to an existing DB.
    # I should probably ask or check first.
    # Given the specificity of the connection, the table likely already exists.
    # Let me assume a common name like 'lecturas' or 'datos'.
    # I'll create a script to inspect the database first to be sure about the table name.

    # For now, I'll write a script to inspect table names.
    pass
