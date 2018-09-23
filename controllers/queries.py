from sqlalchemy.engine import Engine


def get_posts(engine: Engine, post_id: int = None) -> list:
    """
    Get all blog posts as a list of table records

    :param engine: SQLAlchemy engine object
    :param post_id: blog entry 'id' (optional)
    :return: list of post records
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


def get_comments(engine: Engine, post_id, comment_id: int = None) -> list:
    """Get all comments for a specific blog post as a list of table records

    :param engine: SQLAlchemy engine object
    :param post_id: blog entry 'id' (mandatory)
    :param comment_id: comment 'id' (optional)
    :return: list of comment records
    """

    with engine.connect() as conn:
        if comment_id is not None:
            result = conn.execute('SELECT * FROM comments WHERE post_id = ?'
                                  ' AND id = ?', (post_id, comment_id))
        else:
            result = conn.execute('SELECT * FROM comments WHERE post_id = ?',
                                  post_id)

        # unpack results into list of JSON records
        comments = [dict(row) for row in result]

        return comments