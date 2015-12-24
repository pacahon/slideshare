import requests
from six.moves import (urlparse, urlunparse)


def client(api_key, shared_secret, username=None, password=None):
    # Get default session?
    return SlideShareAPI(api_key=api_key, shared_secret=shared_secret, username=username, password=password)


class SlideShareServiceError(Exception):
    pass


class SlideShareAPI(requests.Session):

    BASE_DOMAIN = "www.slideshare.net"

    REQUIRED_CREDENTIALS = [
        'api_key',
        'shared_secret',
    ]

    OPTIONAL_CREDENTIALS = [
        'username',
        'password'
    ]

    _base_url = "https://{}/api/2/".format(BASE_DOMAIN)

    def __init__(self, **options):
        super(SlideShareAPI, self).__init__()
        self.set_credentials(options)

    def set_credentials(self, credentials):
        for kwarg in self.REQUIRED_CREDENTIALS:
            if not credentials.get(kwarg, None):
                raise ValueError("Credential with key '{}' must be specified")
        for kwarg in self.OPTIONAL_CREDENTIALS:
            setattr(self, kwarg, credentials.get(kwarg, None))

    def _url(self, relative_url):
        return "{0}{1}".format(self._base_url, relative_url)

    def _validate_all_known_args(self, actual, allowed):
        for kwarg in actual:
            if kwarg not in allowed:
                raise ValueError(
                    "Invalid args key '{}', must be one of: "
                    "{}".format(kwarg, ', '.join(allowed)))

    def get_slideshow(self, slideshow_id=None, slideshow_url=None, **optional):
        """Get slideshow information by id or url

        Args:
            slideshow_id:
                id of the slideshow to be fetched. Precedence over slideshow_url.
            slideshow_url:
                URL of the slideshow to be fetched. Optional if `slideshow_id` specified
            username:
                username of the requesting user [Optional]
            password:
                password of the requesting user [Optional]
            exclude_tags:
                Exclude tags from the detailed information. 1 to exclude. [Optional]
            detailed:
                Set to True to include optional information.
                Defaults to False. If False only basic information attached [Optional]
        """
        url = self._url('get_slideshow')
        params = {}
        if slideshow_id:
            params["slideshow_id"] = slideshow_id
        elif slideshow_url:
            # FIXME: Are we really needs validate it?
            parsed_url = urlparse(slideshow_url)
            if parsed_url.hostname == self.BASE_DOMAIN:
                params["slideshow_url"] = urlunparse([
                    parsed_url.scheme,
                    parsed_url.netloc,
                    parsed_url.path, '', '', ''
                ])
        else:
            raise ValueError("get_slideshow: slideshow_id or "
                             "slideshow_url must be specified")
        response = self.get(url, params)
        # FIXME: Изучить как ведёт себя ts при кешировании (если поставить запоздалую дату)
        # Proxy?
        # self.request()



    def get_slideshows_by_tag(self, tag, **kwargs):
        pass


