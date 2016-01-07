# python-slideshare

Inspired by https://github.com/cleder/slideshare

Python 3 compatible implementation of Slideshare API with python `requests` module.

WIP!!! Don't try to use it on production.

## How to use

```python
from slideshare import client
slideshare_client = client(api_key=<YOUR_API_KEY>, shared_secret=<YOUR_SHARED_SECRET>)
slideshare_client.slideshow.get_slideshow(slideshow_id=<SLIDESHARE_ID>)
```

## API modules (all WIP)

### slideshow

* get_slideshow
* get_slideshows_by_tag
* get_slideshow_by_group
* get_slideshows_by_user
* search_slideshows
* edit_slideshow
* delete_slideshow
* upload_slideshow

### user

* get_user_favorites
* get_user_contacts
* get_user_groups
* get_user_tags

### favorite
* check_favorite
* add_favorite

### leads

* get_user_campaign_leads
* get_user_campaigns
* get_user_leads


## How to test

You must have extra permissions to pass all tests. For more details about 
extra permissions see `slideshare.slideshow.upload_slideshow` method
 

```
py.test --api_key=<YOUR_API_KEY> --shared_secret=<YOUR_SHARED_SECRET>
```
See `tests/conftest.py` for more details about available options.


<!--python setup.py test-->

## Links

* Slideshare API Documentation http://www.slideshare.net/developers/documentation
* Slideshare Live API http://apiexplorer.slideshare.net/


