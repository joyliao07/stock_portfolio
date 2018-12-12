"""This module defines the routes of stocks app."""
from . import app

# 3rd Party Requirements
from flask import render_template, abort, redirect, url_for, session, g, make_response, request, flash, session
from sqlalchemy.exc import IntegrityError, DBAPIError

# Models
from .models import Company, db

# Forms
from .forms import StockSearchForm, CompanyAddForm

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

        try:
            res = fetch_stock_portfolio(company)
            session['context'] = res.text

            #below lines to validate the result of "res"
            data = json.loads(session['context'])
            company = {
                'symbol': data['symbol'],
            }

            # return redirect(url_for('.portfolio_detail'))
            return redirect(url_for('.preview_company'))

        except JSONDecodeError:
            print('hitting the empty symbol 404')
            print('Json Decode')
            abort(404)

    return render_template('search.html', form=form)



@app.route('/preview', methods=['GET', 'POST'])
def preview_company():
    """
    """
    decoded = json.loads(session['context'])

    form_context = {
        'symbol': decoded['symbol'],
        'name': decoded['companyName'],
    }

    form = CompanyAddForm(**form_context)

    if form.validate_on_submit():
        try:
            data = json.loads(session['context'])
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
        except (DBAPIError, IntegrityError):
            flash('Oops. Something went wrong with your search.')
            return render_template('search.html', form=form)

        return redirect(url_for('.portfolio_detail'))

    return render_template(
        'preview.html',
        form=form,
        symbol=form_context['symbol'],
        name=form_context['name'],
    )


@app.route('/portfolio')
@app.route('/portfolio/<symbol>')
def portfolio_detail():
    """Proxy endpoint for retrieving stock information from a 3rd party API."""
    company = Company.query.all()
    return render_template('portfolio.html', company=company)











# @app.route('/portfolio')
# @app.route('/portfolio/<symbol>')
# def portfolio_detail(symbol=None):
#     """Proxy endpoint for retrieving stock information from a 3rd party API."""

#     try:

#         data = json.loads(session['context'])
#         company = {
#             'symbol': data['symbol'],
#             'companyName': data['companyName'],
#             'exchange': data['exchange'],
#             'industry': data['industry'],
#             'website': data['website'],
#             'description': data['description'],
#             'CEO': data['CEO'],
#             'issueType': data['issueType'],
#             'sector': data['sector'],
#         }
#         new_company = Company(**company)
#         db.session.add(new_company)
#         db.session.commit()

#         return render_template('portfolio.html', company=company)
#     except IntegrityError as e:
#         print(e)
#         res = make_response('That comapny already added :(', 400)
#         return res
