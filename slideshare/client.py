from __future__ import unicode_literals, absolute_import, print_function

import hashlib
import logging
import time

import requests
import xmltodict
from requests.exceptions import RequestException

from slideshare.exceptions import SlideShareError
from slideshare.slideshow import SlideshowMixin

logger = logging.getLogger(__name__)


class SlideShareAPI(requests.Session, SlideshowMixin):

    __API_VERSION__ = 2
    BASE_URL = "https://www.slideshare.net/api/{}/".format(__API_VERSION__)

    def __init__(self,
                 api_key,
                 shared_secret,
                 username=None,
                 password=None,
                 debug_http=False):
        """ Initialize SlideShare API client

        Args:
            api_key (string):
                API key http://www.slideshare.net/developers/applyforapi
            shared_secret (string):
                Shared secret, get it with API key, used to generate
                required `hash` field
            username (string):
                Default username of the requesting user. [Optional]
            password (string):
                Default password of the requesting user. [Optional]
            debug_http (boolean):
                Set to True to enable debug mode. Defaults to False. [Optional]
        """

        # Initialize requests session
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

        self._debug_http = bool(debug_http)
        if self._debug_http:
            import requests.packages.urllib3
            from six.moves import http_client
            # these two lines enable debugging at httplib level
            # (requests->urllib3->httplib)
            # you will see the REQUEST, including HEADERS and DATA, and
            # RESPONSE with HEADERS but without DATA. The only thing missing
            # will be the response.body which is not logged.
            http_client.HTTPConnection.debuglevel = 1
            # you need to initialize logging, otherwise you will not see
            # anything from requests
            logging.basicConfig()
            logger.setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

    def _url(self, relative_url):
        return "{0}{1}".format(self.BASE_URL, relative_url)

    def get(self, url, **kwargs):
        url = self._url(url)
        try:
            response = super(SlideShareAPI, self).get(url, params=kwargs)
            # Raise HTTPError on 40x and 50x
            response.raise_for_status()
        # FIXME: ValueError?
        except (ValueError, RequestException) as e:
            logger.error(e)
            # TODO: extend SlideShareError with ValueError and RequestException?
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
                                                       files=files,
                                                       params=kwargs)
            # Raise HTTPError on 40x and 50x
            response.raise_for_status()
        except (ValueError, RequestException) as e:
            logger.error(e)
            # TODO: add error wrapper
            raise e
        logger.debug(response.content)
        return self.parse_response(response.content)

    @staticmethod
    def parse_response(content):
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

    def prefetch_default_credentials(self, params, options, required=False):
        """ Prefetch default credentials if they are not specified.
        """
        if "username" in options:
            params["username"] = options["username"]
        elif self.username:
            params["username"] = self.username
        elif required:
            raise ValueError("Credentials error: username must be "
                             "provided for this type of request")
        if "password" in options:
            params["password"] = options["password"]
        elif self.password:
            params["password"] = self.password
        elif required:
            raise ValueError("Credentials error: password must be "
                             "provided for this type of request")
        return params
