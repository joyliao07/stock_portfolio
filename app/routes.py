"""This module defines the routes of stocks app."""
from . import app
from .auth import login_required

# 3rd Party Requirements
from flask import render_template, abort, redirect, url_for, session, g, request, flash
from sqlalchemy.exc import IntegrityError, DBAPIError

# Models
from .models import Company, db, Portfolio

# Forms
from .forms import StockSearchForm, CompanyAddForm, PortfolioCreateForm

# API Requests & Other
from json import JSONDecodeError
import requests as req
import json
import os

# helpers

def fetch_stock_portfolio(company):
    """To fetch the return from IEX website."""
    return req.get(f'https://api.iextrading.com/1.0/stock/{ company }/company')



@app.add_template_global
def get_portfolios():
    """
    """
    return Portfolio.query.filter_by(user_id=g.user.id).all()


###############
# CONTROLLERS #
###############


@app.route('/')
def home():
    """To setup the home route."""
    return render_template('home.html', msg='Welcome to the site')


@app.route('/search', methods=['GET', 'POST'])
@login_required
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
            company = {'symbol': data['symbol']}

            return redirect(url_for('.preview_company'))

        except JSONDecodeError:
            print('Json Decode')
            abort(404)

    return render_template('search.html', form=form)



@app.route('/preview', methods=['GET', 'POST'])
@login_required
def preview_company():
    """
    """
    decoded = json.loads(session['context'])

    form_context = {
        'symbol': decoded['symbol'],
        'name': decoded['companyName'],
        'exchange': decoded['exchange'],
        'industry': decoded['industry'],
        'website': decoded['website'],
        'description': decoded['description'],
        'CEO': decoded['CEO'],
        'issueType': decoded['issueType'],
        'sector': decoded['sector'],
    }

    form = CompanyAddForm(**form_context)


    if form.validate_on_submit():
        # THE FORM IS NEVER VALIDATED FROM THE TEST:
        company_dt = [(str(c.symbol)) for c in Company.query.all()]
        if form.data['symbol'] in company_dt:
            print('company already exist!!!')
            flash('Company already in your portfolio.')
            return redirect(url_for('.company_search'))

        try:
            company = Company(
                symbol=form.data['symbol'],
                companyName=form.data['name'],
                exchange=form.data['exchange'],
                industry=form.data['industry'],
                website=form.data['website'],
                description=form.data['description'],
                CEO=form.data['CEO'],
                issueType=form.data['issueType'],
                sector=form.data['sector'],
                portfolio_id=form.data['portfolios'],
            )

            db.session.add(company)
            db.session.commit()

        except (DBAPIError, IntegrityError):
            flash('Oops. Something went wrong with your search.')
            return redirect(url_for('.company_search'))

        return redirect(url_for('.portfolio_detail'))

    return render_template(
        'preview.html',
        form=form,
        symbol=form_context['symbol'],
        name=form_context['name'],
        exchange=form_context['exchange'],
        industry=form_context['industry'],
        website=form_context['website'],
        description=form_context['description'],
        CEO=form_context['CEO'],
        issueType=form_context['issueType'],
        sector=form_context['sector'],
    )

@app.route('/portfolio', methods=['GET', 'POST'])
@app.route('/portfolio/<symbol>', methods=['GET', 'POST'])
@login_required
def portfolio_detail():
    """Proxy endpoint for retrieving stock information from a 3rd party API."""

    form = PortfolioCreateForm()

    if form.validate_on_submit():
        try:
            portfolio = Portfolio(name=form.data['name'], user_id=g.user.id)
            db.session.add(portfolio)
            db.session.commit()
        except (DBAPIError, IntegrityError):
            flash('Oops. Something went wrong with your Portfolio Form.')
            return render_template('portfolio.html', form=form)
        return redirect(url_for('.company_search'))

    user_portfolios = Portfolio.query.filter(Portfolio.user_id == g.user.id).all()
    port_ids = [c.id for c in user_portfolios]

    companies = Company.query.filter(Company.portfolio_id.in_(port_ids)).all()
    return render_template('portfolio.html', companies=companies, form=form)
