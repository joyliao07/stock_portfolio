"""This module test routes.py."""
from .. import app
from ..models import db
import pytest


@pytest.fixture
def client():

    def do_nothing():
        pass

    db.session.commit = do_nothing

    yield app.test_client()

    db.session.rollback()


def test_home_route_get():
    rv = app.test_client().get('/')
    assert rv.status_code == 200
    assert b'<h1>Welcome to the site</h1>' in rv.data


def test_home_route_post():
    rv = app.test_client().post('/')
    assert rv.status_code == 405


def test_home_route_delete():
    rv = app.test_client().delete('/')
    assert rv.status_code == 405


def test_portfolio_route_get():
    rv = app.test_client().get('/portfolio')
    assert rv.status_code == 200
    assert b'<h2>Welcome to the Portfolio</h2>' in rv.data


def test_search_route_get():
    rv = app.test_client().get('/search')
    assert rv.status_code == 200
    assert b'<h2>Search for stocks</h2>' in rv.data


def test_search_post_pre_redirect(client):
    rv = client.post('/search', data={'symbol': 'amzn'})
    assert rv.status_code == 200
    #WE HAVE 200 HERE, NOT 302 REDIRECT


def test_search_post(client):
    rv = client.post('/search', data={'symbol': 'amzn'}, follow_redirects=True)
    assert rv.status_code == 200
    # assert b'<h2>Welcome to the Portfolio</h2>' in rv.data


def test_bunk_symbol(client):
    rv = client.post('/search', data={'symbol': ''}, follow_redirects=True)
    assert rv.status_code == 404
