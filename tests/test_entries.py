from libs.bloglib import EntryFactory
from libs.sqllib import get_posts

ENTRY_ID = 1
ENTRY_TITLE = 'Test blog entry'
ENTRY_TEXT = '<p>Single paragraph</p>'


def test_create_entry(create_entry):
    """Create a blog Entry object and verify its attributes"""

    entry = create_entry(ENTRY_ID, ENTRY_TITLE, ENTRY_TEXT)

    assert entry.id == ENTRY_ID
    assert entry.title == ENTRY_TITLE
    assert entry.content == ENTRY_TEXT


def test_store_entry(create_entry, get_engine):
    """Create a blog entry and store in database"""

    entry = create_entry(ENTRY_ID, ENTRY_TITLE, ENTRY_TEXT)

    entry.to_sql(get_engine)


def test_store_retrieve_entry(create_entry, get_engine):
    """Create a blog entry, store in database and retrieve"""

    entry_in = create_entry(ENTRY_ID, ENTRY_TITLE, ENTRY_TEXT)

    entry_in.to_sql(get_engine)

    # get selected blog entry
    entry_out = EntryFactory.from_sql(get_engine, ENTRY_ID)

    assert entry_in.id == entry_out.id
    assert entry_in.title == entry_out.title
    assert entry_in.content == entry_out.content


def test_store_retrieve_entry_multiple(create_entry, get_engine):
    """Create several blog entries, store in database and retrieve"""

    create_entry(ENTRY_ID, ENTRY_TITLE, ENTRY_TEXT).to_sql(get_engine)
    create_entry(ENTRY_ID + 1, ENTRY_TITLE, ENTRY_TEXT).to_sql(get_engine)
    create_entry(ENTRY_ID + 2, ENTRY_TITLE, ENTRY_TEXT).to_sql(get_engine)

    posts = get_posts(get_engine)

    for i in range(len(posts)):
        assert posts[i]['id'] == i + 1
        assert posts[i]['title'] == ENTRY_TITLE
        assert posts[i]['content'] == ENTRY_TEXT


def test_entry_from_file():
    """Create blog entry from HTML file"""

    entry = EntryFactory.from_file('tests/fixtures/test_entry.html')

    assert entry.id
    assert entry.title
    assert entry.content
