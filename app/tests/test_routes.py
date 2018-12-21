from flask import g, session
from ..routes import fetch_stock_portfolio


class TestClass:
    @classmethod
    def setup_class(cls):
        pass

    def test_home_route_get(self, app):
        """To test / with 200."""
        # QUESTION - RV GET DROPPED AFTER THE FIRST ASSERT??????
        rv = app.test_client().get('/')
        assert rv.status_code == 200
        assert b'<h1 class="home-h1">Welcome to the site</h1>' in app.test_client().get('/').data


    def test_home_route_post(self, app):
        """Test home route."""
        rv = app.test_client().post('/')
        assert rv.status_code == 405


    def test_search_route_get_without_redirects(self, app):
        """To test /search with 302."""
        rv = app.test_client().get('/search')
        assert rv.status_code == 302
        # rv = app.test_client().get('/search')


    def test_search_route_get_with_redirect(self, app):
        """To test /search with 200."""
        rv = app.test_client().get('/search', follow_redirects=True)
        assert rv.status_code == 200


    def test_search_get_method(self, app, user):
        """To test /search with 200."""
        # TO TEST ROUTES.PY LINE 33, 52-54, 69-71

        # use 'with' statement to keep context
        with app.test_client() as client:

            # set session's user_id
            with client.session_transaction() as flask_session:
                flask_session['user_id'] = user.id
                # user == <User default@example.com>   user.id == 1

            # navigate to protected route
            rv = client.get('/search')

            # auth module's @app.before_request should result in
            # g.user being set
            assert g.user == user

            # good login gives 200
            assert rv.status_code == 200


    def test_search_with_post(self, app, user, portfolio, company):
        """To test /search with 200."""
        # TO TEST ROUTES.PY LINE 25, 55 - 67

        with app.test_client() as client:
            with client.session_transaction() as flask_session:
                flask_session['user_id'] = user.id
                flask_session['portfolio_id'] = portfolio.id
                flask_session['symbol'] = company.symbol

        rv = client.post('/search')
        assert client.get('/search').status_code == 200


    def test_search_with_post_404(self, app, user, portfolio, company):
        """To test /search with invalid company symbol."""
        # TO TEST ROUTES.PY LINE 67 - 69.. does not hit the lines

        with app.test_client() as client:
            with client.session_transaction() as flask_session:
                flask_session['user_id'] = user.id
                flask_session['portfolio_id'] = portfolio.id
                flask_session['symbol'] = '111111111'

        assert client.post('/search', follow_redirects=True).status_code == 200


    def test_preview_get(self, app, user, portfolio, company):
        """To test /preivew with valid company symbol."""
        # TO TEST ROUTES.PY LINE 80-97, 119-120

        with app.test_client() as client:
            with client.session_transaction() as flask_session:
                flask_session['user_id'] = user.id
                flask_session['portfolio_id'] = portfolio.id
                flask_session['symbol'] = company.symbol

        client.post('/search')
        assert client.get('/preview').status_code == 200


    def test_add_fresh_company_to_portfolio_redirect(self, authenticated_client, portfolio):
        """Add a fresh company and follow redirect"""

        # need to first post from search page in order to add company stock symbol to session
        authenticated_client.post('/search', data={'symbol': 'goog'}, follow_redirects=True)

        # simulate form input
        form_data = {'symbol': 'goog', 'companyName': 'Alphabet Inc.', 'portfolios': portfolio.id}

        rv = authenticated_client.post('/preview', data=form_data, follow_redirects=True)
        assert rv.status_code == 200

        # confirm proper markup
        assert b'<h2>Search for stocks</h2>' in authenticated_client.post('/preview', data=form_data, follow_redirects=True).data

    def test_candlestick_chart(self, authenticated_client):
        """See the candlestick chart of..."""

        rv = authenticated_client.get('/candlestick_chart/aapl')
        assert rv.status_code == 200

        # confirm proper markup
        assert b'<h2>See the candlestick chart.</h2>' in authenticated_client.get('/candlestick_chart/aapl').data

    def test_stock_chart(self, authenticated_client):
        """See the stock chart of..."""

        rv = authenticated_client.get('/stock_chart/aapl')
        assert rv.status_code == 200

        # confirm proper markup
        assert b'<h2>See the stocks chart.</h2>' in authenticated_client.get('/stock_chart/aapl').data

    def test_portfolio_add_new(self, authenticated_client, portfolio):
        """Add a fresh portfolio and follow redirect"""
        # simulate form input
        form_data = {'name': 'new investment'}

        rv = authenticated_client.post('/portfolio', data=form_data, follow_redirects=True)

        assert rv.status_code == 200

    def test_registration_200(self, client):
        """To test /register with 200."""
        res = client.get('/register')
        assert res.status_code == 200

    def test_registration_with_actual_name_and_password(self, client):
        """To test /register with POST."""
        res = client.post(
            '/register',
            data={'email': 'test@example.com', 'password': 'seekret'},
            follow_redirects=True,
        )
        assert res.status_code == 200
