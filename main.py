import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template
from sqlalchemy import create_engine

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

    # get 'published' posts from database
    posts = [post for post in get_posts(engine) if post['published']]

    # create website context
    context = {'posts': posts}

    # generate endpoint
    return render_template('index.html', **context)


@app.route('/<post_id>')
def posts(post_id):
    """Individual blog post endpoints"""

    # get post from database
    posts = [post for post in get_posts(engine) if post['published']]

    context = {'posts': posts}

    # extract information on selected post
    for post in posts:
        if int(post_id) == post['id']:

            # include 'post' attributes in Web page 'context'
            context.update(post)

            return render_template(post['filename'], **context)

    return render_template('not_found.html', **context)


if __name__ == '__main__':
    # create database connector
    engine = create_engine(f'sqlite:///{SQL_DB}')

    # generate tables (if missing)
    create_tables(engine)

    # start Web application
    app.run(os.environ.get('FLASK_HOST'),
            os.environ.get('FLASK_PORT'),
            debug=True)
