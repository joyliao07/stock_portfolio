import pytest
from .. models import db, Company

@pytest.fixture
def session():

    def do_nothing():
        pass

    db.session.commit = do_nothing

    yield db.session

    db.session.rollback()



