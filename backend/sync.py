import asyncio
import logging
from sqlalchemy.orm import Session
from datetime import datetime
from . import crud, database, models

logger = logging.getLogger(__name__)


async def sync_worker():
    """Background task to sync data from MySQL to SQLite using Timestamps."""
    print("Starting Sync Worker (Timestamp-based)...")

    try:
        print("Bootstrapping: Attempting to fetch last 100 records by DATE...")

        db_mysql = database.SessionMySQL()
        db_sqlite = database.SessionSQLite()

        # 1. Bootstrap: Get latest 100 records by date
        initial_records = crud.get_remote_records_batch(db_mysql, limit=100)

        synced_count = 0
        if initial_records:
            print(f"Found {len(initial_records)} records in remote DB.")
            for record in initial_records:
                try:
                    if crud.create_local_record(db_sqlite, record):
                        synced_count += 1
                except Exception as e:
                    print(f"Failed to copy record {record.fecha}: {e}")

            print(f"Bootstrapping complete. Synced {synced_count} new records.")
        else:
            print("Bootstrapping: No records returned from remote.")

        db_mysql.close()
        db_sqlite.close()

    except Exception as e:
        print(f"Error during bootstrapping: {e}")

    # --- Continuous Sync Loop ---
    while True:
        try:
            db_mysql = database.SessionMySQL()
            db_sqlite = database.SessionSQLite()

            try:
                # 1. Get latest local timestamp
                last_date = crud.get_last_synced_date(db_sqlite)

                # If no data locally (failed bootstrap?), set a very old date
                if not last_date:
                    last_date = datetime(2000, 1, 1)

                # 2. Fetch records strictly newer than last_date
                new_records = crud.get_new_remote_records_by_date(db_mysql, last_date)

                if new_records:
                    print(
                        f"Live Sync: Found {len(new_records)} new records (Newer than {last_date})..."
                    )
                    for record in new_records:
                        crud.create_local_record(db_sqlite, record)

            except Exception as e:
                print(f"Error during sync cycle: {e}")
            finally:
                db_mysql.close()
                db_sqlite.close()

        except Exception as e:
            print(f"Critical Worker Error: {e}")

        # Wait 2 seconds
        await asyncio.sleep(2)
