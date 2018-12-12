# Flask-WTF Forms
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


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







