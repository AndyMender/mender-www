from flask import Flask
from sqlalchemy import create_engine

from libs.sqllib import create_tables, get_posts

app = Flask(__name__)

SQLDB = 'mender.db'

if __name__ == '__main__':
    engine = create_engine(f'sqlite:///{SQLDB}')

    create_tables(engine)

    # app.run()