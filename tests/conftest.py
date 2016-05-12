import os
import pytest

from distutils import dir_util

from slideshare.client import SlideShareAPI


def pytest_addoption(parser):
    parser.addoption("--api_key", action="store", required=True,
                     help="Set this to the API Key that SlideShare "
                          "has provided for you")
    parser.addoption("--shared_secret", action="store", required=True,
                     help="Shared secret that SlideShare has provided for you")
    parser.addoption("--username", action="store", default="",
                     help="Default username of the requesting user")
    parser.addoption("--password", action="store", default="",
                     help="Default password of the requesting user")
    parser.addoption("--debug_http", action="store_true",
                     help="Debug all http requests")
    parser.addoption("--slideshow_id", action="store", required=True,
                     help="ID of existed slideshow.")


@pytest.fixture(scope="session")
def client(request):
    api_key = request.config.getoption("--api_key")
    shared_secret = request.config.getoption("--shared_secret")
    username = request.config.getoption("--username")
    password = request.config.getoption("--password")
    debug_http = request.config.getoption("--debug_http")
    return SlideShareAPI(api_key=api_key,
                         shared_secret=shared_secret,
                         username=username,
                         password=password,
                         debug_http=debug_http)


@pytest.fixture(scope="session")
def slideshow(request, client):
    # TODO: make slideshow_id optional
    slideshow_id = request.config.getoption("--slideshow_id")
    response = client.get_slideshow(slideshow_id=slideshow_id)
    assert response['Slideshow']['ID'] == slideshow_id

    class SlideShow(object):
        pass

    slideshow = SlideShow()
    slideshow.id = response['Slideshow']['ID']
    slideshow.title = response['Slideshow']['Title']
    slideshow.url = response['Slideshow']['URL']
    return slideshow


# Inspired by http://stackoverflow.com/a/29631801/1341309
@pytest.fixture()
def datadir(tmpdir, request):
    """
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    """
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir
