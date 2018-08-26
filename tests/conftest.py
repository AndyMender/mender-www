import pytest
from sqlalchemy import create_engine

from libs.bloglib import Entry
from libs.sqllib import create_tables


@pytest.fixture
def get_engine():
    """Provide a temporary SQLAlchemy engine connection
    to an in-memory database for tests"""

    engine = create_engine(f'sqlite://')

    create_tables(engine)

    conn = engine.connect()

    yield conn

    conn.close()
    engine.dispose()


@pytest.fixture
def create_entry():
    """Create a blog Entry object from provided params"""

    def _create_entry(id: int, title: str, content: str, tags: list):
        return Entry(id, title, content, tags)

    return _create_entry
