import pytest
from slideshare.client import SlideShareAPI


def pytest_addoption(parser):
    parser.addoption("--api_key", action="store", required=True,
        help="Set this to the API Key that SlideShare has provided for you")
    parser.addoption("--shared_secret", action="store", required=True,
        help="Shared secret that SlideShare has provided for you")
    parser.addoption("--username", action="store", default="",
        help="Default username of the requesting user")
    parser.addoption("--password", action="store", default="",
        help="Default password of the requesting user")
    parser.addoption("--debug_http", action="store_true",
        help="Debug all http requests")

@pytest.fixture
def client(request):
    api_key = request.config.getoption("--api_key")
    shared_secret = request.config.getoption("--shared_secret")
    username = request.config.getoption("--username")
    password = request.config.getoption("--password")
    debugHTTP = request.config.getoption("--debug_http")
    return SlideShareAPI(api_key=api_key, shared_secret=shared_secret, username=username, password=password,
                         debugHTTP=debugHTTP)
