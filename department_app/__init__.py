from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

import os

MIGRATION_DIR = os.path.join('department_app', 'migrations')
app = Flask(__name__)

from dotenv import load_dotenv

load_dotenv('.env')

app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=MIGRATION_DIR)

from department_app.views import departments_view
from department_app.views import employees_view
from department_app.views import errors_view

# logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')

file_handler = logging.FileHandler(filename='app.log', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

app.logger.handlers.clear()
app.logger.addHandler(file_handler)
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.DEBUG)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.handlers.clear()
werkzeug_logger.addHandler(file_handler)
werkzeug_logger.addHandler(stream_handler)
werkzeug_logger.setLevel(logging.DEBUG)
