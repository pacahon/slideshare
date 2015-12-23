import requests


def client(api_key, shared_secret, username=None, password=None):
    # Get default session?
    return SlideShareAPI(api_key=api_key, shared_secret=shared_secret, username=username, password=password)


class SlideShareServiceError(Exception):
    pass

# TODO store session in attribute
class SlideShareAPI(requests.Session):

    _base_url = "https://www.slideshare.net/api/2/"

    REQUIRED_CREDENTIALS = [
        'api_key',
        'shared_secret',
    ]

    OPTIONAL_CREDENTIALS = [
        'username',
        'password'
    ]

    def __init__(self, **options):
        super(SlideShareAPI, self).__init__()
        self.set_credentials(options)

    def set_credentials(self, credentials):
        for kwarg in self.REQUIRED_CREDENTIALS:
            if kwarg not in credentials or not credentials.get(kwarg, None):
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

    def get(self, url):
        pass

    def patch(self, url):
        pass

    def delete(self, url):
        pass

    def post(self, url):
        pass

    def get_slideshow(self, slideshow_id=None, slideshow_url=None, **optional):
        url = self._url('get_slideshow')
        params = {}
        if slideshow_id:
            params["slideshow_id"] = slideshow_id
        elif slideshow_url:
            params["slideshow_url"] = slideshow_url
        else:
            raise ValueError("get_slideshow: slideshow_id or slideshow_url must be specified")


    def get_slideshows_by_tag(self, tag, **kwargs):
        pass


