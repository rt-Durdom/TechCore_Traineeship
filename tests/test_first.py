TEXT = 'SELECT 1'

def test_db_session(db_session):
    result = db_session.execute(TEXT).scalar()
    assert result == 1

def multi(a, b):
    return a * b


def test_multi():
    assert multi(2, 3) == 6


def summm(a, b):
    return a + b


def test_simple_add():
    assert summm(1, 1) == 2
