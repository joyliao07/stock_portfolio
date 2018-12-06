###########
# IMPORTS #
###########
# Generic Flask Requirements
from flask import Flask


import os

basedir = os.path.abspath(os.path.dirname(__file__))

######################
# APPLICATION SETUPS #
######################
# `flask run` - runs application on local server
app = Flask(__name__, static_url_path='', static_folder='static', instance_relative_config=True)

app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)


from ..app import routes, forms, models, exceptions
