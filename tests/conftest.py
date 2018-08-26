import os

import pytest
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine

from libs.bloglib import Entry

# load .env file
load_dotenv(find_dotenv())

# SQLite3 database
SQLDB = os.environ.get('SQL_DB')


@pytest.fixture
def sql_engine():
    """Provide a temporary SQLAlchemy engine connection for tests"""

    engine = create_engine(f'sqlite:///{SQLDB}')

    conn = engine.connect()

    yield conn

    conn.close()


@pytest.fixture
def create_entry():
    """Create a blog Entry object from provided params"""

    def _create_entry(id: int, title: str, content: str):
        return Entry(id, title, content)

    return _create_entry
