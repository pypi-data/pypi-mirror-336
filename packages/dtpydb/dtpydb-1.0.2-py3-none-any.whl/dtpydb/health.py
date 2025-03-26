from sqlalchemy import text
from .database import DatabaseInstance


def is_database_connected(db: DatabaseInstance) -> tuple[bool, Exception | None]:
    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True, None

    except Exception as e:
        return False, e
