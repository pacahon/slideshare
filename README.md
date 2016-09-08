# python-slideshare

Python 2/3 compatible version of Slideshare API.

## How to use

```python
from slideshare.client import SlideShareAPI
slideshare_client = SlideShareAPI(api_key=<YOUR_API_KEY>,
                                  shared_secret=<YOUR_SHARED_SECRET>)
slideshare_client.get_slideshow(slideshow_id=<SLIDESHARE_ID>)
```

## Implemented methods

* get_slideshow
* get_slideshows_by_tag
* delete_slideshow
* upload_slideshow (partially tested)
* edit_slideshow (not tested at all)

TODO:

* get_slideshow_by_group
* get_slideshows_by_user
* search_slideshows
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
pip install pytest
```

You must have extra permissions to pass all tests. For more details about 
extra permissions see `slideshare.upload_slideshow` method

```
py.test --api_key=<YOUR_API_KEY> --shared_secret=<YOUR_SHARED_SECRET> --slideshare_id=<ALREADY_UPLOADED_SLIDESHARE_ID>
```

See `tests/conftest.py` for more details about available options.

## Docs

```
pip installsphinxcontrib-napoleon==0.4.3
pip install sphinx_rtd_theme
```

And then:

```
cd docs/
make html
```


## Links

* Slideshare API Documentation http://www.slideshare.net/developers/documentation
* Slideshare Live API http://apiexplorer.slideshare.net/ (dead?!)


