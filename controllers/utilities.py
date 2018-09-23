from sqlalchemy.engine import Engine


def database_setup(engine: Engine) -> bool:
    """Optimize SQLite database for use as a Web backend

    :param engine: SQLAlchemy engine object
    :return: True on success, False on failure
    """

    # init SQL query
    sql_query = 'PRAGMA journal_mode=WAL;'

    with engine.connect() as conn:
        conn.execute(sql_query)

    return True
