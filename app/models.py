
# DB-Related Imports
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from flask_migrate import Migrate
from . import app


db = SQLAlchemy(app)
migrate = Migrate(app, db)


##########
# MODELS #
##########
# `flask db init` - Creates migrations directory and configs  (ONLY RUN ONCE)
# `flask db migrate -m 'migration message'` - creates migrations and preps DB
# `flask db upgrade` - creates tables

# temporarily remove "unique=True" from symbol and companyName??


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.ForeignKey('portfolios.id'), nullable=False)
    symbol = db.Column(db.String(64), index=True, unique=True)
    companyName = db.Column(db.String(256), index=True, unique=True)
    exchange = db.Column(db.String(128))
    industry = db.Column(db.String(128))
    website = db.Column(db.String(128))
    description = db.Column(db.Text)
    CEO = db.Column(db.String(128))
    issueType = db.Column(db.String(128))
    sector = db.Column(db.String(128))

    date_created = db.Column(db.DateTime, default=dt.now())

    def __repr__(self):
        return '<Company {}>'.format(self.companyName)


class Portfolio(db.Model):
    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)

    companies = db.relationship('Company', backref='portfolio', lazy=True)

    date_created = db.Column(db.DateTime, default=dt.now())

    def __repr__(self):
        return '<Portfolio {}>'.format(self.name)
