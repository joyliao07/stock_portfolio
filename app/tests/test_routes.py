"""This module test routes.py."""
from .. import app
from ..models import db
import pytest


@pytest.fixture
def client():
    """Fixture to test database by passing an empty do_nothing."""
    def do_nothing():
        pass

    db.session.commit = do_nothing

    yield app.test_client()

    db.session.rollback()


def test_home_route_get():
    """To test home route returns status code 200."""
    rv = app.test_client().get('/')
    assert rv.status_code == 200
    assert b'<h1>Welcome to the site</h1>' in rv.data


def test_home_route_post():
    """To test home route does not have post method."""
    rv = app.test_client().post('/')
    assert rv.status_code == 405


def test_home_route_delete():
    """To test home route does not have delete method."""
    rv = app.test_client().delete('/')
    assert rv.status_code == 405


def test_portfolio_route_get():
    """To test portfolio return a 200 status code."""
    rv = app.test_client().get('/portfolio')
    assert rv.status_code == 200
    assert b'<h2>Welcome to the Portfolio</h2>' in rv.data


def test_search_route_get():
    """To test search return a 200 status code."""
    rv = app.test_client().get('/search')
    assert rv.status_code == 200
    assert b'<h2>Search for stocks</h2>' in rv.data


def test_search_post_pre_redirect(client):
    """To test search's redirect before redict, returns a 302 status code."""
    rv = client.post('/search', data={'symbol': 'amzn'})
    assert rv.status_code == 302


def test_search_post(client):
    """To test search's POST method returns a 200 status code."""
    rv = client.post('/search', data={'symbol': 'amzn'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'<h2>Welcome to the Portfolio</h2>' in rv.data


def test_bunk_symbol(client):
    """To test an empty sumbol returns a 404 status code."""
    rv = client.post('/search', data={'symbol': ''}, follow_redirects=True)
    assert rv.status_code == 404
