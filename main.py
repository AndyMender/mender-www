import os
import uuid

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from sqlalchemy import create_engine

from controllers.tables import create_tables
from controllers.utilities import database_setup
from views.routes import build_endpoints

# load ENV from .env file
load_dotenv(find_dotenv())

# set up Flask application
app = Flask(__name__,
            static_folder='public',
            template_folder='templates')

# configure application
app.config.from_object(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())

DB = os.environ.get('SQL_DB')

if __name__ == '__main__':
    # create database connector
    engine = create_engine(f'sqlite:///{DB}', isolation_level="AUTOCOMMIT")

    # set up database for Web app use
    database_setup(engine)

    # generate tables (if missing)
    create_tables(engine)

    # set up application endpoints and URL paths
    build_endpoints(app, engine)

    # start Web application
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
    )
