import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, abort
from sqlalchemy import create_engine

from libs.bloglib import Entry
from libs.sqllib import create_tables, get_posts

# load .env file
load_dotenv(find_dotenv())

# set up Flask application
app = Flask(__name__,
            static_folder='public',
            template_folder='templates')

SQL_DB = os.environ.get('SQL_DB')


@app.route('/')
def index():
    """Blog front page"""

    # get posts from database
    posts = get_posts(engine)

    # create website context
    context = {'posts': posts}

    # generate endpoint
    return render_template('index.html', **context)


@app.route('/<post_id>')
def posts(post_id):
    """Individual blog post endpoints"""

    # get post from database
    posts = get_posts(engine)

    context = {'posts': posts}

    # extract information on selected post
    for post in posts:
        if int(post_id) == post['id']:

            # create website context
            context['title'] = post['title']
            context['tags'] = post['tags']
            context['publish_date'] = post['timestamp']

            return render_template(post['filename'], **context)

    return abort(404)


if __name__ == '__main__':
    # create database connector
    engine = create_engine(f'sqlite:///{SQL_DB}')

    # generate tables (if missing)
    create_tables(engine)

    # create selected post and store in database
    entry = Entry(post_id=1, title='Test Post', filename='001.html', tags=['test'])
    entry.to_sql(engine)

    # start Web application
    app.run(os.environ.get('FLASK_HOST'),
            os.environ.get('FLASK_PORT'),
            debug=True)
