from . import app

# 3rd Party Requirements
from flask import render_template, abort, redirect, url_for, session, g, make_response
from sqlalchemy.exc import IntegrityError

# Models
from .models import db, City

# Forms
from .forms import CitySearchForm
from .forms import StockSearchForm

# API Requests & Other
from json import JSONDecodeError
import requests as req
import json
import os

# helpers


# def fetch_city_weather(city):
#     """
#     """
#     return req.get(f"{os.getenv('API_URL')}{city}&APPID={os.getenv('API_KEY')}")

def fetch_stock_portfolio(company):
    """
    """
    return req.get(f"{os.getenv('API_URL')}{company}/book")


###############
# CONTROLLERS #
###############


@app.route('/')
def home():
    """
    """
    return render_template('home.html', msg='Brr...')


@app.route('/search', methods=['GET', 'POST'])
def city_search():
    """Proxy endpoint for retrieving city information from a 3rd party API.
    """
    # form = CitySearchForm()

    # if form.validate_on_submit():
    #     city = form.data['city_name']

    #     res = fetch_city_weather(city)

    #     try:
    #         session['context'] = res.text
    #         return redirect(url_for('.city_detail'))

    #     except JSONDecodeError:
    #         abort(404)

    # return render_template('search.html', form=form)

    form = StockSearchForm()

    if form.validate_on_submit():
        company = form.data['company_name']

        res = fetch_stock_portfolio(company)

        try:
            session['context'] = res.text
            # return render_template('home.html', msg='Search Result Found.')
            return redirect(url_for('.city_detail'))

        except JSONDecodeError:
            abort(404)

    return render_template('search.html', form=form)

@app.route('/city')
@app.route('/city/<company_name>')
def city_detail(company_name=None):

    if company_name:
        res = fetch_stock_portfolio(company_name)
        return render_template('city_detail.html', **res.json())

    else:

        try:
            context = json.loads(session['context'])
            city = City(cityName=context['quote']['companyName'])
            print(context)
            # print('city', city)
            # db.session.add(city)
            # db.session.commit()
            # return render_template('city_detail.html', **context)
            # return redirect(......)
            # return redirect('stock_detail.html', **res.json())
            return redirect(url_for('.portfolio'))
            return 'temp'
        except IntegrityError as e:
            print(e)
            res = make_response('That city already added :(', 400)
            return res


@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    """Proxy endpoint for retrieving stock information from a 3rd party API.
    """

    return render_template('portfolio.html')




















