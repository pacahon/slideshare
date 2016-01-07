from __future__ import unicode_literals, absolute_import, print_function

import logging
import hashlib
import requests
import time
import xmltodict
from requests.exceptions import ConnectTimeout, ConnectionError

from slideshare.slideshow import Slideshow

logger = logging.getLogger(__name__)
# TODO: NullPointer handler?
# TODO: Add cache?


def client(*args, **kwargs):
    """Returns SlideShareAPI instance. See SlideShareAPI for details"""
    return SlideShareAPI(*args, **kwargs)


class SlideShareError(Exception):
    """ SlideShare API Error Code.
    See details on http://www.slideshare.net/developers/documentation
    """
    def __init__(self, errno, errmsg):
        self.errno = errno
        self.errmsg = errmsg

    def __str__(self):
        return "SlideShareError {}: {}".format(self.errno, self.errmsg)


class SlideShareAPI(requests.Session):

    __API_VERSION__ = 2
    BASE_URL = "https://www.slideshare.net/api/{}/".format(__API_VERSION__)

    def __init__(self,
                 api_key,
                 shared_secret,
                 username=None,
                 password=None,
                 debugHTTP=False):
        """ Initialize SlideShare API client

        Args:
            api_key (string):
                API key http://www.slideshare.net/developers/applyforapi
            shared_secret (string):
                Shared secret, get it with API key, used to generate required `hash` field
            username (string):
                Default username of the requesting user. [Optional]
            password (string):
                Default password of the requesting user. [Optional]
            debugHTTP (boolean):
                Set to True to enable debug mode. Defaults to False. [Optional]

        """
        # TODO: add description
        # Initialize session
        super(SlideShareAPI, self).__init__()

        required_list = [api_key, shared_secret]
        if not all(required_list):
            raise ValueError("Api initialization error: "
                             "api key and shared secret must be provided")
        # Set api key for all future requests
        self.params["api_key"] = api_key

        self.shared_secret = shared_secret
        # Default credentials
        self.username = username
        self.password = password

        self._debugHTTP = bool(debugHTTP)
        if self._debugHTTP:
            import requests.packages.urllib3
            from six.moves import http_client
            # these two lines enable debugging at httplib level (requests->urllib3->httplib)
            # you will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
            # the only thing missing will be the response.body which is not logged.
            http_client.HTTPConnection.debuglevel = 1

            logging.basicConfig()  # you need to initialize logging, otherwise you will not see anything from requests
            logger.setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

        # Bind api methods
        self.slideshow = Slideshow(self)

    def _url(self, relative_url):
        return "{0}{1}".format(self.BASE_URL, relative_url)

    def get(self, url, **kwargs):
        url = self._url(url)
        try:
            response = super(SlideShareAPI, self).get(url, params=kwargs)
        except (ConnectionError, ValueError, ConnectTimeout) as e:
            logger.error(e)
            # FIXME: processing errors? What to do with this crap? :<
            raise e
        logger.debug(response.content)
        return self.parse_response(response.content)

    def post(self, url, data=None, json=None, **kwargs):
        url = self._url(url)
        try:
            files = None
            if "files" in kwargs:
                files = kwargs["files"]
                del kwargs["files"]
            response = super(SlideShareAPI, self).post(url, data, json,
                                                       files=files, **kwargs)
        except (ConnectionError, ValueError, ConnectTimeout) as e:
            logger.error(e)
            # FIXME: If want only reraise, remove try/except block?
            raise e
        logger.debug(response.content)
        return self.parse_response(response.content)

    def parse_response(self, content):
        data = xmltodict.parse(content)
        if data.get('SlideShareServiceError'):
            logger.debug(data)
            raise SlideShareError(
                data['SlideShareServiceError']['Message']['@ID'],
                data['SlideShareServiceError']['Message']['#text'])
        return data

    def prepare_request(self, request):
        """ Overrides requests.Session method. All requests in addition
        to `api_key` must provide `ts` and `hash` parameters
        """
        timestamp = int(time.time())
        self.params["ts"] = timestamp
        hash = self.shared_secret + str(timestamp)
        self.params["hash"] = hashlib.sha1(hash.encode("utf-8")).hexdigest()
        return super(SlideShareAPI, self).prepare_request(request)

    def prefetch_default_credentials(self, params, options):
        """ Prefetch default credentials if they are not specified
        """
        if "username" in options:
            params["username"] = options["username"]
        elif self.username:
            params["username"] = self.username
        if "password" in options:
            params["password"] = options["password"]
        elif self.password:
            params["password"] = self.password
        return params
