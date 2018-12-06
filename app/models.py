from . import app

# DB-Related Imports
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import datetime as dt


db = SQLAlchemy(app)
migrate = Migrate(app, db)


##########
# MODELS #
##########
# `flask db init` - Creates migrations directory and configs  (ONLY RUN ONCE)
# `flask db migrate -m 'migration message'` - creates migrations and preps DB
# `flask db upgrade` - creates tables
class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    cityName = db.Column(db.String(256), index=True, unique=True)
    date_created = db.Column(db.DateTime, default=dt.now())

    def __repr__(self):
        return '<City {}>'.format(self.cityName)


# class Company(db.Model):
#     __tablename__ = 'companies'

#     symbol = db.Column(db.String(64), index=True, unique=True)
#     CEO = db.Column(db.String(64))

#     dated_created = db.Column(db.DateTime, default=dt.now())

#     def __repr__(self):
#         return '<Company {}>'.format(self.companyName)

