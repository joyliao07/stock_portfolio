from . import app

# 3rd Party Requirements
from flask import render_template, abort, redirect, url_for, session, g, make_response, request
from sqlalchemy.exc import IntegrityError

# Models
from .models import Company, db

# Forms
from .forms import StockSearchForm

# API Requests & Other
from json import JSONDecodeError
import requests as req
import json
import os

# helpers


def fetch_stock_portfolio(company):
    """
    """
    return req.get(f'https://api.iextrading.com/1.0/stock/{ company }/company')


###############
# CONTROLLERS #
###############


@app.route('/')
def home():
    """
    """
    return render_template('home.html', msg='Welcome to the site')


@app.route('/search', methods=['GET', 'POST'])
def company_search():
    """Proxy endpoint for retrieving city information from a 3rd party API.
    """

    form = StockSearchForm()

    # TO CHECK 1) IF THE METHOD IS POST, AND 2) IF THE DATA UPDATED IN THE FORM IS VALID:
    if request.method == 'POST':
        company = form.data['symbol']
        res = fetch_stock_portfolio(company)

        try:
            data = json.loads(res.text)

            company = {
                'symbol': data['symbol'],
                'companyName': data['companyName'],
                'exchange': data['exchange'],
                'industry': data['industry'],
                'website': data['website'],
                'description': data['description'],
                'CEO': data['CEO'],
                'issueType': data['issueType'],
                'sector': data['sector'],
            }
            print('company: ', company)

            new_company = Company(**company)
            db.session.add(new_company)
            db.session.commit()

            return redirect(url_for('.portfolio_detail'))

        except JSONDecodeError:
            print('Json Decode')
            abort(404)

    return render_template('search.html', form=form)

# @app.route('/city')
# @app.route('/city/<symbol>')
# def portfolio_detail(symbol=None):

#     if symbol:
#         res = fetch_stock_portfolio(symbol)
#         return render_template('portfolio_detail.html', **res.json())

#     else:

#         try:
#             context = json.loads(session['context'])
#             city = City(cityName=context['quote']['companyName'])
#             print(context)
#             # print('city', city)
#             # db.session.add(city)
#             # db.session.commit()
#             # return render_template('portfolio_detail.html', **context)
#             # return redirect(......)
#             # return redirect('stock_detail.html', **res.json())
#             return redirect(url_for('.portfolio'))
#             return 'temp'
#         except IntegrityError as e:
#             print(e)
#             res = make_response('That city already added :(', 400)
#             return res


@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio_detail():
    """Proxy endpoint for retrieving stock information from a 3rd party API.
    """


    return render_template('portfolio.html')
