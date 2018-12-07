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
    symbol = StringField('company symbol', validators=[DataRequired()])










