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
                     '  filename TEXT NOT NULL,'
                     '  tags TEXT,'
                     '  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
                     '  published BOOLEAN DEFAULT FALSE,'
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


def get_posts(engine: Engine, post_id: int = None) -> list:
    """
    Get all blog posts as a list of table records

    :param engine: SQLAlchemy engine object
    :param post_id: blog entry 'id' (optional)
    :return:
    """
    with engine.connect() as conn:
        if post_id is not None:
            result = conn.execute('SELECT * FROM entries WHERE id = ?',
                                  post_id)
        else:
            result = conn.execute('SELECT * FROM entries')

        # unpack results into list of JSON records
        posts = [dict(row) for row in result]

        # data correctly retrieved
        if len(posts) > 0:

            # unpack post 'tags'
            for i in range(len(posts)):
                posts[i]['tags'] = posts[i]['tags'].split(',')

        return posts
