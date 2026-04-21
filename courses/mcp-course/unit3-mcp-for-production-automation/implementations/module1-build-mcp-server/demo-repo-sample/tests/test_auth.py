from app.auth import login


def test_login_success():
    assert login("admin", "admin") is True
