import logging
import os.path
from typing import Optional

import lxml.html
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text

from .sqllib import get_posts


class Entry:
    """Blog entry object representation"""
    def __init__(self, id: int, title: str, content: str, tags: list = None):
        self.id = id
        self.title = title
        self.content = content
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
                         ' (id, title, content, tags)'
                         ' VALUES (:id, :title, :content, :tags)')

        data = {'id': self.id,
                'title': self.title,
                'content': self.content,
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

        # entry for specified 'id' does not exist
        if len(posts) == 0:
            return None

        post = posts[0]

        return Entry(post['id'], post['title'],
                     post['content'], post['tags'])

    @staticmethod
    def from_html(html: str) -> Entry:
        """Generate an Entry object from a loaded HTML string

        :param html: HTML file loaded into a string
        :return:
        """
        document = lxml.html.document_fromstring(html)

        # get entry 'id'
        id = int(document.head.get('id'))

        # get entry 'title'
        title = ''
        for child in document.head.iterchildren():
            if child.tag == 'title':
                title = child.text
                break

        # get entry 'content'
        content = ''.join(lxml.html.tostring(child, pretty_print=True).decode()
                          for child in document.body.iterchildren())

        # get entry 'tags'
        tags = document.head.get('id')
        if tags is None:
            tags = ""

        return Entry(id, title, content, tags.split(','))

    @staticmethod
    def from_file(filename: str) -> Entry:
        """Generate an Entry object from an HTML file

        :param filename: HTML file name
        """
        ext = os.path.splitext(filename)[1]

        if ext not in ('.html', '.HTML'):
            raise ValueError(f'{filename} is not an HTML file.')

        return EntryFactory.from_html(open(filename).read())
