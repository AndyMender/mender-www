from datetime import datetime

from sqlalchemy.engine import Engine
from sqlalchemy.sql import text


# TODO: Functions like this don't need to return anything
def database_setup(engine: Engine) -> bool:
    """Optimize SQLite database for use as a Web backend

    :param engine: SQLAlchemy engine object
    :return: True on success, False on failure
    """

    # init SQL query
    sql_query = text("PRAGMA journal_mode=WAL;")

    with engine.connect() as conn:
        conn.execute(sql_query)

    return True


def date_now() -> str:
    """Return current UTC date as string in ISO 8601 format"""
    return datetime.utcnow().strftime('%Y-%m-%d')


def time_now() -> str:
    """Return current UTC timestamp as string in ISO 8601 format"""
    return datetime.utcnow().isoformat(sep=' ', timespec='seconds')
