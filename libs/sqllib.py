from sqlalchemy.engine import Engine


def create_tables(engine: Engine) -> bool:
    """
    Create tables for blog entries and user comments

    :param engine: SQLAlchemy engine object
    :return:
    """
    with engine.connect() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS entries'
                     ' (id INTEGER PRIMARY KEY,'
                     '  title TEXT NOT NULL,'
                     '  content TEXT NOT NULL,'
                     '  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
                     '  UNIQUE (id, title) ON CONFLICT REPLACE'
                     '  )')

    with engine.connect() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS comments'
                     ' (id INTEGER PRIMARY KEY AUTOINCREMENT,'
                     '  name TEXT,'
                     '  post_id INTEGER,'
                     '  content TEXT,'
                     '  FOREIGN KEY (post_id) REFERENCES entries(id)'
                     '  )')

    return True