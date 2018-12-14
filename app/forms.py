# Flask-WTF Forms
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired
from .models import Portfolio


#########
# FORMS #
#########


class StockSearchForm(FlaskForm):
    """
    Form to search on IEX.
    """
    symbol = StringField('Company Symbol', validators=[DataRequired()])


class CompanyAddForm(FlaskForm):
    """
    """
    symbol = StringField('Company Symbol', validators=[DataRequired()])
    name = StringField('Company', validators=[DataRequired()])
    portfolios = SelectField('portfolios')
    exchange = StringField('exchange', validators=[DataRequired()])
    industry = StringField('industry', validators=[DataRequired()])
    website = StringField('website', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    CEO = StringField('CEO', validators=[DataRequired()])
    issueType = StringField('issueType', validators=[DataRequired()])
    sector = StringField('sector', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.portfolios.choices = [(str(p.id), p.name) for p in Portfolio.query.all()]


class PortfolioCreateForm(FlaskForm):
    """
    """
    name = StringField('name', validators=[DataRequired()])


class AuthForm(FlaskForm):
    """
    """
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

