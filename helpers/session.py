from curl_cffi import requests

session = None


def get_session():
    global session
    if session is None:
        session = requests.Session(impersonate="chrome")
    return session


def new_session():
    return requests.Session(impersonate="chrome")
