from sqlalchemy.engine import Engine


def create_table_posts(engine: Engine) -> bool:
    """Create table for blog entries/posts

    :param engine: SQLAlchemy engine object
    :return: True on success, False on failure
    """

    sql_query = ('CREATE TABLE IF NOT EXISTS entries'
                 ' (id INTEGER PRIMARY KEY,'
                 '  title TEXT NOT NULL,'
                 '  filename TEXT NOT NULL,'
                 '  tags TEXT,'
                 '  publish_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
                 '  published INTEGER DEFAULT 0,'
                 '  UNIQUE (id, title) ON CONFLICT REPLACE'
                 '  )')

    with engine.connect() as conn:
        conn.execute(sql_query)

    return True


def create_table_comments(engine: Engine) -> bool:
    """Create table for user comments

    :param engine: SQLAlchemy engine object
    :return: True on success, False on failure
    """

    sql_query = ('CREATE TABLE IF NOT EXISTS comments'
                 ' (id INTEGER PRIMARY KEY AUTOINCREMENT,'
                 '  name TEXT,'
                 '  occupation TEXT,'
                 '  email TEXT,'
                 '  post_id INTEGER,'
                 '  content TEXT,'
                 '  publish_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
                 '  approved INTEGER DEFAULT 0,'
                 '  FOREIGN KEY (post_id) REFERENCES entries(id)'
                 '  )')

    with engine.connect() as conn:
        conn.execute(sql_query)

    return True


def create_table_stats(engine: Engine) -> bool:
    """Create table for storing application statistics

    :param engine: SQLAlchemy engine object
    :return: True on success, False on failure
    """

    sql_query = ('CREATE TABLE IF NOT EXISTS stats'
                 ' (id INTEGER PRIMARY KEY AUTOINCREMENT,'
                 '  tick_date DATE DEFAULT CURRENT_TIMESTAMP,'
                 '  page_views INTEGER'
                 '  )')

    with engine.connect() as conn:
        conn.execute(sql_query)

    return True


def create_tables(engine: Engine) -> bool:
    """
    Create SQL tables for Web application

    :param engine: SQLAlchemy engine object
    :return: True on success, False on failure
    """

    create_table_posts(engine)
    create_table_comments(engine)
    create_table_stats(engine)

    return True