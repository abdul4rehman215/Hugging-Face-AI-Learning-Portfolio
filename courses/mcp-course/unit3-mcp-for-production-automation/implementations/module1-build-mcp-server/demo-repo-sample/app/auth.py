import hashlib


def login(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    expected = hashlib.sha256("admin".encode()).hexdigest()
    return username == "admin" and hashed == expected
