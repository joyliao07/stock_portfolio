# Flask-WTF Forms
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.portfolios.choices = [(str(p.id), p.name) for p in Portfolio.query.all()]


class PortfolioCreateForm(FlaskForm):
    """
    """
    name = StringField('name', validators=[DataRequired()])



