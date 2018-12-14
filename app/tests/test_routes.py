class TestClass:
    @classmethod
    def setup_class(cls):
        pass

    def test_home_route_get(self, app):
        rv = app.test_client().get('/')
        assert rv.status_code == 200
        assert b'<h1>Welcome to the site</h1>' in rv.data

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











