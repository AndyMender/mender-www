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


def get_posts(engine: Engine, id: int = None) -> list:
    """
    Get all blog posts as a list of table records

    :param engine: SQLAlchemy engine object
    :return:
    """
    with engine.connect() as conn:
        if id is not None:
            result = conn.execute('SELECT * FROM entries WHERE id = ?',
                                  id)
        else:
            result = conn.execute('SELECT * FROM entries')

        # no data retrieved
        if len(result[0]) == 0:
            return []

        return [dict(row) for row in result]

