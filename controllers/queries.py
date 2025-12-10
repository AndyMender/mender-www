from typing import Union

from sqlalchemy.engine import Engine
from sqlalchemy.sql import text

from controllers.utilities import date_now


def get_posts(engine: Engine, post_id: int = None) -> list:
    """
    Get all blog posts as a list of table records

    :param engine: SQLAlchemy engine object
    :param post_id: blog entry 'id' (optional)
    :return: list of post records
    """

    with engine.connect() as conn:
        if post_id is not None:
            result = conn.execute(
                text("SELECT * FROM entries WHERE id = :id"),
                {"id": post_id}
            )
        else:
            result = conn.execute(text("SELECT * FROM entries"))

        # unpack results into list of JSON records
        # TODO: Implement lazy-loading instead?
        posts = [dict(row) for row in result.mappings().all()]

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
            result = conn.execute(
                text("SELECT * FROM comments WHERE post_id = :post_id AND id = :id"),
                {"post_id": post_id, "id": comment_id},
            )
        else:
            result = conn.execute(
                text("SELECT * FROM comments WHERE post_id = :post_id"),
                {"post_id": post_id},
            )

        # unpack results into list of JSON records
        comments = [dict(row) for row in result.mappings().all()]

        return comments


def get_page_views(engine: Engine, mode: str = 'current') -> Union[int, None]:
    """Get page views for current date or all

    :param engine: SQLAlchemy engine object
    :param mode: page view aggregation method ('current', 'all')
    """

    # SQL query return placeholder
    result = []

    # get page views from database
    with engine.connect() as conn:
        if mode == 'all':
            result = conn.execute(text("SELECT total(page_views) FROM stats"))
        elif mode == 'current':
            result = conn.execute(
                text("SELECT page_views FROM stats WHERE tick_date = :tick_date"),
                {"tick_date": date_now()},
            )

        # unpack results into list of JSON records
        result = [dict(row) for row in result.mappings().all()]

        # check results and return sanitized value
        if len(result) > 0:
            return int(list(result[0].values())[0])
        else:
            return None
