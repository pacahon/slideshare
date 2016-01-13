from slideshare.client import SlideShareAPI

__version__ = '0.0.1'


def client(*args, **kwargs):
    """Returns SlideShareAPI instance."""
    return SlideShareAPI(*args, **kwargs)