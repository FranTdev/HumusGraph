from sqlalchemy import create_engine, inspect

# Database credentials
SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://demia:proyectodemia2026@132.148.182.196/vermicompost"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
inspector = inspect(engine)

try:
    tables = inspector.get_table_names()
    print("Tables in database:", tables)

    # If the user mentioned specific columns, I should check which table has them.
    expected_cols = {"id", "fecha", "temperatura", "humedad", "ph"}

    for table in tables:
        columns = inspector.get_columns(table)
        col_names = {c["name"] for c in columns}
        print(f"Table '{table}' columns: {col_names}")

        if expected_cols.issubset(col_names):
            print(f"FOUND MATCHING TABLE: {table}")

except Exception as e:
    print(f"Error inspecting database: {e}")
