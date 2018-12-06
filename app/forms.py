# Flask-WTF Forms
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


#########
# FORMS #
#########
class CitySearchForm(FlaskForm):
    """
    Eentsy Weentsy Form that has a single, required 'name' field
    """
    city_name = StringField('name', validators=[DataRequired()])


class StockSearchForm(FlaskForm):
    """
    Form to search on IEX.
    """
    company_name = StringField('name', validators=[DataRequired()])










