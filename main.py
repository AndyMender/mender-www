import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template
from sqlalchemy import create_engine

from libs.bloglib import EntryFactory
from libs.sqllib import create_tables, get_posts

# load .env file
load_dotenv(find_dotenv())

# set up Flask application
app = Flask(__name__,
            static_url_path='',
            static_folder='public',
            template_folder='templates')

SQL_DB = os.environ.get('SQL_DB')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    engine = create_engine(f'sqlite:///{SQL_DB}')

    create_tables(engine)

    app.run(os.environ.get('FLASK_HOST'),
            os.environ.get('FLASK_PORT'),
            debug=True)
