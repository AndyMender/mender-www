from typing import Optional

from sqlalchemy.engine import Engine

from controllers.sql import get_comments, get_posts
from models.models import Comment, Entry


class CommentFactory:
    """Factory class to generate comments"""
    @staticmethod
    def from_sql(engine: Engine, post_id: int, comment_id: int) -> Optional[Comment]:
        """Generate a Comment object from a SQL table

        :param engine: SQLAlchemy engine object
        :param post_id: Entry identifier in comments table
        :param comment_id: Comment identifier in comments table
        :return: populated Comment object
        """
        comments = get_comments(engine, post_id, comment_id)

        comment = None

        # populate comment if 'id' exists
        if len(comments) > 0:
            c = comments[0]

            comment = Comment(c['post_id'],
                              c['name'],
                              c['content'],
                              c['email'])

        return comment


class EntryFactory:
    """Factory class to generate entries"""
    @staticmethod
    def from_sql(engine: Engine, id: int) -> Optional[Entry]:
        """Generate an Entry object from a SQL table

        :param engine: SQLAlchemy engine object
        :param id: Entry identifier in table
        :return: populated Entry object
        """
        posts = get_posts(engine, id)

        entry = None

        # populate entry if 'id' exists
        if len(posts) > 0:
            post = posts[0]

            entry = Entry(post['id'],
                          post['title'],
                          post['filename'],
                          post['tags'])

        return entry
