# python-slideshare


Inspired by https://github.com/cleder/slideshare

Python 3 compatible implementation of Slideshare API based on `requests` module.

# WIP!!! Don't try to use it on production.

## How to use

```python
from slideshare import client
slideshare_client = client(api_key=<YOUR_API_KEY>, shared_secret=<YOUR_SHARED_SECRET>)
slideshare_client.get_slideshow(slideshow_id=<SLIDESHARE_ID>)
```

## API modules

* get_slideshow (tested)
* get_slideshows_by_tag (tested)

TODO:

* get_slideshow_by_group
* get_slideshows_by_user
* search_slideshows
* edit_slideshow
* delete_slideshow (tested)
* upload_slideshow (partially tested)
* get_user_favorites
* get_user_contacts
* get_user_groups
* get_user_tags
* check_favorite
* add_favorite
* get_user_campaign_leads
* get_user_campaigns
* get_user_leads


## How to test

```
pip installsphinxcontrib-napoleon==0.4.3
pip install sphinx_rtd_theme
```

You must have extra permissions to pass all tests. For more details about 
extra permissions see `slideshare.upload_slideshow` method
 

```
py.test --api_key=<YOUR_API_KEY> --shared_secret=<YOUR_SHARED_SECRET> --slideshare_id=<ALREADY_UPLOADED_SLIDESHARE_ID>
```

See `tests/conftest.py` for more details about available options. (TODO: write about all available options here in more details)

## TODO:

* add cache for get requests? 

## Links

* Slideshare API Documentation http://www.slideshare.net/developers/documentation
* Slideshare Live API http://apiexplorer.slideshare.net/


