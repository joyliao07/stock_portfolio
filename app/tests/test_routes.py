from flask import g


class TestClass:
    @classmethod
    def setup_class(cls):
        pass

    def test_home_route_get(self, app):
        # QUESTION - RV GET DROPPED AFTER THE FIRST ASSERT??????
        rv = app.test_client().get('/')
        assert rv.status_code == 200
        assert b'<h1 class="home-h1">Welcome to the site</h1>' in app.test_client().get('/').data


    def test_home_route_post(self, app):
        rv = app.test_client().post('/')
        assert rv.status_code == 405


    def test_search_route_get(self, app):
            rv = app.test_client().get('/search')
            assert rv.status_code == 302
            # assert b'<h2>Search for stocks</h2>' in rv.data

    # "session" does not work becuase now requires login.
    # def test_search_post_pre_redirect(self, app, session):
    #     rv = app.test_client().post('/search', data = {'symbol' : 'amzn'})
    #     assert rv.status_code == 302

    def test_protected_route_with_user_fixture(self, app, user):
        """
        Using the user fixture's id
        add it to the current session.
        This should trigger the auth to load user with the given user_id
        add store it in 'g'
        after that protected routes should be reachable
        """
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


    def test_search_with_api_request(self, app, user, portfolio):
        # TO TEST ROUTES.PY LINE 57 - 65

        with app.test_client() as client:
            with client.session_transaction() as flask_session:
                flask_session['user_id'] = user.id



                # flask_session['portfolio_id'] = portfolio.portfolio_id
                # flask_session['company'] = company.id



        import pdb; pdb.set_trace()
        rv = client.get('/search')



            # auth module's @app.before_request should result in
            # g.user being set
            # assert g.company == user

            # good login gives 200
            # assert rv.status_code == 200

            # assert g.company ==











    # def test_search_with_incorrect_company_symbol(self, app, user):
    #     """
    #     Using the user fixture's id
    #     add it to the current session.
    #     This should trigger the auth to load user with the given user_id
    #     add store it in 'g'
    #     after that protected routes should be reachable
    #     """

    #     # use 'with' statement to keep context
    #     with app.test_client() as client:

    #         # set session's user_id
    #         with client.session_transaction() as flask_session:
    #             flask_session['user_id'] = user.id

    #         # navigate to protected route
    #         rv = client.get('/search')

    #         # auth module's @app.before_request should result in
    #         # g.user being set
    #         assert g.user == user

    #         # good login gives 200
    #         assert rv.status_code == 200









