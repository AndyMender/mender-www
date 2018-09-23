from werkzeug.datastructures import MultiDict
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text

from controllers.queries import get_page_views
from controllers.utilities import date_now
from models.forms import CommentForm
from models.models import Comment


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


def update_page_views(engine: Engine) -> None:
    """Increment page views

    :param engine: SQLAlchemy engine object
    :return:
    """
    # get current page_views value if it exists
    page_views = get_page_views(engine, mode='current')

    # update page views
    with engine.connect() as conn:

        # no page_views for current date? new entry
        if page_views is None:
            sql_query = text('INSERT INTO stats (tick_date, page_views)'
                             ' VALUES (:tick_date, :page_views)')

            data = {'tick_date': date_now(),
                    'page_views': 1}

            conn.execute(sql_query, **data)

        # increment page_views count
        else:
            sql_query = text('UPDATE stats SET page_views = :page_views'
                             ' WHERE tick_date = :tick_date')

            data = {'tick_date': date_now(),
                    'page_views': page_views + 1}

            conn.execute(sql_query, **data)
