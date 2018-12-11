"""This module defines the routes of stocks app."""
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
    """To fetch the return from IEX website."""
    return req.get(f'https://api.iextrading.com/1.0/stock/{ company }/company')


###############
# CONTROLLERS #
###############


@app.route('/')
def home():
    """To setup the home route."""
    return render_template('home.html', msg='Welcome to the site')


@app.route('/search', methods=['GET', 'POST'])
def company_search():
    """Proxy endpoint for retrieving city information from a 3rd party API."""

    form = StockSearchForm()

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

            new_company = Company(**company)
            db.session.add(new_company)
            db.session.commit()

            return render_template('portfolio.html', company=company)

        except JSONDecodeError:
            print('Json Decode')
            abort(404)

    return render_template('search.html', form=form)


# @app.route('/portfolio', methods=['GET', 'POST'])
# def portfolio_detail(symbol=None):
#     """Proxy endpoint for retrieving stock information from a 3rd party API."""
#     print('symbol in portfolio: ', symbol)
#     if symbol:
#         res = fetch_stock_portfolio(symbol)
#         print('the first category')
#         return render_template('portfolio_detail.html', **res.json())

#     else:
#         try:
#             print('the second category')
#             res = fetch_stock_portfolio(symbol)
#             session['context'] = res.text
#             context = json.loads(session['context'])
#             company = Company(symbol=context['symbol'])
#             # print('company', company) is None
#             return render_template('portfolio.html', **context)
#         except IntegrityError as e:
#             print(e)
#             res = make_response('That city already added :(', 400)
#             return res

#     return render_template('portfolio.html')
