from werkzeug.datastructures import MultiDict
from sqlalchemy.engine import Engine

from models.forms import CommentForm
from models.models import Comment


def create_tables(engine: Engine) -> bool:
    """
    Create tables for blog entries and user comments

    :param engine: SQLAlchemy engine object
    :return: True on success, False on failure
    """
    with engine.connect() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS entries'
                     ' (id INTEGER PRIMARY KEY,'
                     '  title TEXT NOT NULL,'
                     '  filename TEXT NOT NULL,'
                     '  tags TEXT,'
                     '  publish_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
                     '  published INTEGER DEFAULT 0,'
                     '  UNIQUE (id, title) ON CONFLICT REPLACE'
                     '  )')

    with engine.connect() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS comments'
                     ' (id INTEGER PRIMARY KEY AUTOINCREMENT,'
                     '  name TEXT,'
                     '  occupation TEXT,'
                     '  email TEXT,'
                     '  post_id INTEGER,'
                     '  content TEXT,'
                     '  publish_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
                     '  approved INTEGER DEFAULT 0,'
                     '  FOREIGN KEY (post_id) REFERENCES entries(id)'
                     '  )')

    return True


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


def store_comment(post_id: int, request: MultiDict, engine: Engine) -> str:
    """Extract comment information from request object; validate and store

    :param post_id: post 'id' to which the comment refers
    :param request: Flask request object
    :param engine: SQLAlchemy engine object
    """

    # fill in comment form
    form = CommentForm(request.form)

    # validate response, comment and store comment in database
    if request.method == 'POST':
        if form.validate():
            comment = Comment(post_id,
                              request.form.get('name'),
                              request.form.get('content'),
                              request.form.get('email'),
                              request.form.get('occupation'))

            if comment.to_sql(engine):
                return 'success'

        # indicate source of error on failed validation
        elif len(request.form.get('content')) > 1000:
            return 'Comment too long. A maximum of 1000 characters is allowed.'
        elif len(request.form.get('content')) < 5:
            return 'Comment too short. At least 5 characters are required.'
        elif len(request.form.get('name')) > 20:
            return 'Name too long. A maximum of 20 characters is allowed.'
        elif len(request.form.get('email')) > 50:
            return 'Email address too long. A maximum of 50 characters is allowed.'
        elif len(request.form.get('email')) < 5:
            return 'Email address too short. At least 5 characters are required.'
        elif len(request.form.get('occupation')) > 100:
            return 'Occupation name too long. A maximum of 100 characters is allowed.'

    return ''