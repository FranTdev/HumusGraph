from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import SensorMySQL

MYSQL_URL = "mysql+pymysql://demia:proyectodemia2026@132.148.182.196/vermicompost"
engine = create_engine(MYSQL_URL)
Session = sessionmaker(bind=engine)
session = Session()

try:
    count = session.query(SensorMySQL).count()
    print(f"Total: {count}")

    last_5 = session.query(SensorMySQL).order_by(SensorMySQL.id.desc()).limit(5).all()
    for r in last_5:
        print(f"ID:{r.id}, Date:{r.fecha}")

except Exception as e:
    print(e)
finally:
    session.close()
