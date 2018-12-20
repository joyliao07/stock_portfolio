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

# Numpy & Charts
import numpy as np
from datetime import datetime
import pandas as pd
import numpy.polynomial.polynomial as poly
import bokeh.plotting as bk
from bokeh.models import HoverTool, Label, BoxZoomTool, PanTool, ZoomInTool, ZoomOutTool, ResetTool
from pandas.plotting._converter import DatetimeConverter
# import matplotlib
# import matplotlib.pyplot as plt


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
        existing_symbol = [(str(c.symbol)) for c in Company.query.filter(Company.portfolio_id == form.data['portfolios']).all()]
        if form.data['symbol'] in existing_symbol:
            flash('Company already in your portfolio.')
            return redirect(url_for('.company_search'))

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

    user_portfolios = Portfolio.query.filter(Portfolio.user_id==g.user.id).all()
    port_ids = [c.id for c in user_portfolios]



    companies = Company.query.filter(Company.portfolio_id.in_(port_ids)).all()
    return render_template('portfolio.html', companies=companies, form=form)


@app.route('/candlestick_chart', methods=['GET', 'POST'])
# @login_required
def candlestick_chart():
    """To generate a candlestick chart of the chosen company."""

    if 1 == 1:
        # 5 YEARS OF HISTORY IS AVAILABLE
        data = json.loads(session['context'])
        company_symbol = data['symbol']

        res = req.get(f'https://api.iextrading.com/1.0/stock/{company_symbol}/chart/5y')
        data_5_year = res.json()

        # PASS DATA INTO DATAFRAME
        df = pd.DataFrame(data_5_year)

        df['date_pd'] = pd.to_datetime(df.date)
        df['year'] = df.date_pd.dt.year
        seqs = np.arange(df.shape[0])
        df['seqs'] = pd.Series(seqs)

        df['mid'] = (df.high + df.low) // 2

        df['height'] = df.apply(
            lambda x: x['close'] - x['open'] if x['close'] != x['open'] else 0.01,
            axis=1
        )

        inc = df.close > df.open
        dec = df.close < df.open
        w = .3

        sourceInc = bk.ColumnDataSource(df.loc[inc])
        sourceDec = bk.ColumnDataSource(df.loc[dec])

        hover = HoverTool(
            tooltips=[
                ('Date', '@date'),
                ('Low', '@low'),
                ('High', '@high'),
                ('Open', '@open'),
                ('Close', '@close'),
                ('Mid', '@mid'),
            ]
        )

        TOOLS = [hover, BoxZoomTool(), PanTool(), ZoomInTool(), ZoomOutTool(), ResetTool()]

        # PLOTTING THE CHART
        p = bk.figure(plot_width=1200, plot_height=800, title= f'{company_symbol}' , tools=TOOLS, toolbar_location='above')

        p.xaxis.major_label_orientation = np.pi/4
        p.grid.grid_line_alpha = w
        descriptor = Label(x=70, y=70, text='5-Year Data Of Your Chosen Company')
        p.add_layout(descriptor)

        # CHART LAYOUT
        p.segment(df.seqs[inc], df.high[inc], df.seqs[inc], df.low[inc], color='green')
        p.segment(df.seqs[dec], df.high[dec], df.seqs[dec], df.low[dec], color='red')
        p.rect(x='seqs', y='mid', width=w, height='height', fill_color='red', line_color='red', source=sourceDec)
        p.rect(x='seqs', y='mid', width=w, height='height', fill_color='green', line_color='green', source=sourceInc)










        return render_template('candlestick_chart.html')
    else:
        # 5-YEAR DATA IS NOT AVAILABLE
        flash('Company does not have a 5-year history.')
        return redirect(url_for('.company_search'))



@app.route('/stock_chart', methods=['GET', 'POST'])
# @login_required
def stock_chart():
    """To generate a stock chart of the chosen company."""

    return render_template('stock_chart.html')
    # if 0
    #     # IF THE CHOSEN COMPANY IS VALID
    #     # pass
    # else:
        # GENERATE A CANDLESTICK CHART HERE


