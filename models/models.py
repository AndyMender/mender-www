import logging

from sqlalchemy.engine import Engine
from sqlalchemy.sql import text


# TODO: Add Post model?
class Comment:
    """Blog entry comment object representation"""
    def __init__(self, post_id: int, name: str, content: str, email: str = None,
                 occupation: str = None):
        self.post_id = post_id
        self.name = name
        self.content = content
        self.email = email
        self.occupation = occupation

    def get_logger(self):
        """Create logger object for the class"""
        return logging.getLogger(self.__class__.__name__)

    def to_sql(self, engine: Engine) -> bool:
        """Send comment to database table via provided engine

        :param engine: SQLAlchemy engine object
        :return: True on success, False on failure
        """
        sql_query = text('INSERT OR REPLACE INTO comments'
                         ' (name, occupation, email, post_id, content)'
                         ' VALUES (:name, :occupation, :email, :post_id, :content)')

        data = {'name': self.name,
                'occupation': self.occupation,
                'email': self.email,
                'post_id': self.post_id,
                'content': self.content}

        with engine.connect() as conn:
            conn.execute(sql_query, data)

        return True


class Entry:
    """Blog entry object representation"""
    def __init__(self, post_id: int, title: str, filename: str, tags: list = None):
        self.id = post_id
        self.title = title
        self.filename = filename
        self.tags = tags if tags is not None else []
        self.logger = self.get_logger()

    def get_logger(self):
        """Create logger object for the class"""
        return logging.getLogger(self.__class__.__name__)

    def to_sql(self, engine: Engine) -> bool:
        """Send entry to database table via provided engine

        :param engine: SQLAlchemy engine object
        :return: True on success, False on failure
        """
        sql_query = text('INSERT OR REPLACE INTO entries'
                         ' (id, title, filename, tags)'
                         ' VALUES (:id, :title, :filename, :tags)')

        data = {'id': self.id,
                'title': self.title,
                'filename': self.filename,
                'tags': ','.join(self.tags)}

        with engine.connect() as conn:
            conn.execute(sql_query, data)

        return True