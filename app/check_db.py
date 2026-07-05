from sqlalchemy import inspect
from app.db.session import engine

def main() -> None:
    inspector = inspect(engine)
    print("\nTables:")
    for table in inspector.get_table_names():
        print(f" - {table}")

if __name__ == "__main__":
    main()