from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import SensorLocal
from datetime import datetime

SQLITE_URL = "sqlite:///./local_storage.db"
engine = create_engine(SQLITE_URL)
Session = sessionmaker(bind=engine)
session = Session()

try:
    print("--- Inspecting Local SQLite ---")
    count = session.query(SensorLocal).count()
    print(f"Total Records: {count}")

    last_10 = (
        session.query(SensorLocal).order_by(SensorLocal.fecha.desc()).limit(10).all()
    )
    if last_10:
        print("\nLatest 10 records:")
        for r in last_10:
            print(f"Date: {r.fecha} | T: {r.temperatura} | H: {r.humedad} | pH: {r.ph}")
    else:
        print("\nNo records found.")

except Exception as e:
    print(e)
finally:
    session.close()
