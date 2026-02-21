import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# MySQL Database (Remote/Local)
MYSQL_URL = os.getenv(
    "MYSQL_URL", "mysql+pymysql://user:password@localhost/vermicompost"
)
engine_mysql = create_engine(MYSQL_URL, pool_pre_ping=True, pool_recycle=3600)
SessionMySQL = sessionmaker(autocommit=False, autoflush=False, bind=engine_mysql)

# SQLite Database (Local)
SQLITE_URL = os.getenv("SQLITE_URL", "sqlite:///./local_storage.db")
engine_sqlite = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
SessionSQLite = sessionmaker(autocommit=False, autoflush=False, bind=engine_sqlite)

Base = declarative_base()


def get_mysql_db():
    db = SessionMySQL()
    try:
        yield db
    finally:
        db.close()


def get_sqlite_db():
    db = SessionSQLite()
    try:
        yield db
    finally:
        db.close()
