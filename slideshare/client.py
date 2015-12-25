
import logging
import hashlib
import requests
from requests.exceptions import ConnectTimeout, ConnectionError
import time

import xmltodict
from six.moves.urllib.parse import (urlparse, urlunparse)

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

    def _url(self, relative_url):
        return "{0}{1}".format(self.BASE_URL, relative_url)

    def get(self, url, **kwargs):
        try:
            response = super(SlideShareAPI, self).get(url, params=kwargs)
        except (ConnectionError, ValueError, ConnectTimeout) as e:
            logger.error(e)
            # FIXME: processing errors? What to do with this crap? :<
            raise e
        logger.debug(response.content)
        data = xmltodict.parse(response.content)
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

    def get_slideshow(self, slideshow_id=None, slideshow_url=None, **optional):
        """Get slideshow information by id or url

        Args:
            slideshow_id (int):
                id of the slideshow to be fetched. Precedence over slideshow_url.
            slideshow_url (string):
                URL of the slideshow to be fetched. Optional if `slideshow_id` specified
            username (string):
                username of the requesting user [Optional]
            password (string):
                password of the requesting user [Optional]
            exclude_tags (boolean):
                Exclude tags from the detailed information. 1 to exclude. [Optional]
            detailed (boolean):
                Set to 1 to include optional information (tags, for example)
                Defaults to None. If None only basic information attached [Optional]

        """
        url = self._url('get_slideshow')
        params = {}
        if slideshow_id:
            params["slideshow_id"] = slideshow_id
        elif slideshow_url:
            params["slideshow_url"] = slideshow_url
        else:
            raise ValueError("get_slideshow: slideshow_id or "
                             "slideshow_url must be specified")

        if "exclude_tags" in optional:
            params["exclude_tags"] = int(bool(optional["exclude_tags"]))

        if "detailed" in optional:
            params["detailed"] = int(bool(optional["detailed"]))

        params.update(self.params)
        return self.get(url, **params)



    def get_slideshows_by_tag(self, tag, **optional):
        """ Get slideshows by tag

        Args:
            tag (string):
                tag name
            limit (int):
                specify number of items to return. Default to 10. [Optional]
            offset (int):
                specify offset [Optional]
            detailed (boolean):
                Set to 1 to include optional information (tags, for example)
                Defaults to None. If None only basic information attached [Optional]

        """
        url = self._url('get_slideshows_by_tag')
        params = {}
        params["tag"] = tag

        if "limit" in optional:
            try:
                params["limit"] = int(optional.get("limit"))
            except ValueError:
                raise ValueError("get_slideshows_by_tag: invalid "
                                 "value for {}".format(optional.get("limit")))
        else:
            params["limit"] = 10

        if "offset" in optional:
            try:
                params["offset"] = int(optional.get("offset"))
            except ValueError:
                raise ValueError("get_slideshows_by_tag: invalid "
                                 "value for {}".format(optional.get("offset")))

        if "detailed" in optional:
            params["detailed"] = int(bool(optional["detailed"]))

        return self.get(url, **params)

    def upload_slideshow(self):
        """Upload slideshow

        Note: This method requires extra permissions. If you want to
        upload a file using SlideShare API, please send an email to
        api@slideshare.com with your developer account username
        describing the use case.

        """




x = client(api_key="OX5YoPYg", shared_secret="R3lITlTK", username="pacahon", password="q3wcp9", debugHTTP=True)
# y = x.get_slideshow(slideshow_id="56441607", exclude_tags=False, detailed=True)
# print("DETAILED")
# print(y)
print('-----------')
y = x.get_slideshows_by_tag("crisis", limit=1)
print(y)
print("END")