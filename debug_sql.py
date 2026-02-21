from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

MYSQL_URL = "mysql+pymysql://demia:proyectodemia2026@132.148.182.196/vermicompost"
engine = create_engine(MYSQL_URL)
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Use raw SQL to be sure about what we are seeing without model assumptions
    with engine.connect() as con:
        print("--- Table Info ---")
        rs = con.execute(text("SELECT COUNT(*) FROM sensores"))
        print(f"Count: {rs.fetchone()[0]}")

        print("\n--- Latest 5 by Date ---")
        rs = con.execute(
            text("SELECT id, fecha FROM sensores ORDER BY fecha DESC LIMIT 5")
        )
        for row in rs:
            print(f"ID: {row[0]}, Date: {row[1]}")

        print("\n--- Latest 5 by ID ---")
        rs = con.execute(
            text("SELECT id, fecha FROM sensores ORDER BY id DESC LIMIT 5")
        )
        for row in rs:
            print(f"ID: {row[0]}, Date: {row[1]}")

except Exception as e:
    print(e)
finally:
    session.close()
