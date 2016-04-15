import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

#db for local developement
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/db_dev'
db = SQLAlchemy(app)

#db for cloud
#heroku = Heroku(app)
#db = SQLAlchemy(app)
