import logging
import os.path
from typing import Optional

import lxml.html
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text

from libs.sqllib import get_posts


class Entry:
    """Blog entry object representation"""
    def __init__(self, post_id: int, title: str, filename: str, tags: list = None):
        self.post_id = post_id
        self.title = title
        self.filename = filename
        self.tags = tags if tags is not None else []
        self.logger = self.get_logger()

    def get_logger(self):
        """Create logger object for the class"""
        return logging.getLogger(self.__class__.__name__)

    def to_sql(self, engine: Engine) -> bool:
        """
        Send entry to database table via provided engine

        :param engine: SQLAlchemy engine object
        :return:
        """
        sql_query = text('INSERT OR REPLACE INTO entries'
                         ' (id, title, filename, tags)'
                         ' VALUES (:id, :title, :filename, :tags)')

        data = {'id': self.post_id,
                'title': self.title,
                'filename': self.filename,
                'tags': ','.join(self.tags)}

        with engine.connect() as conn:
            conn.execute(sql_query, **data)

        return True


class EntryFactory:
    """Factory class to generate entries"""
    @staticmethod
    def from_sql(engine: Engine, id: int) -> Optional[Entry]:
        """Generate an Entry object from a SQL table

        :param engine: SQLAlchemy engine object
        :param id: Entry identifier in table
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
