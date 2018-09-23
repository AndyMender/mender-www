import pytest
from sqlalchemy import create_engine

from models.models import Entry
from controllers.sql import create_tables


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

    def _create_entry(id: int, title: str, filename: str, tags: list = None):
        return Entry(id, title, filename, tags)

    return _create_entry
