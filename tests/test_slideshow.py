# TODO: first upload, get id, then get!s
import pytest


def test_upload_slideshow_by_upload_url(client):
    upload_url = "https://github.com/pacahon/slideshare/raw/master/tests/slide.pdf"
    slideshow_title = "Slideshow Title"
    response = client.slideshow.upload_slideshow(slideshow_title,
                                                 upload_url=upload_url)
    assert "SlideShowUploaded" in response
    assert "SlideShowID" in response["SlideShowUploaded"]


def test_get_slideshow_by_id(client):
    slideshow_id = '56441607'
    response = client.slideshow.get_slideshow(slideshow_id=slideshow_id)
    assert response['Slideshow']['ID'] == slideshow_id


def test_get_slideshow_by_id_with_detail(client):
    pass


def test_get_slideshow_by_url(client):
    pass
    # sls = api.get_slideshow(slideshow_url=
    #                         "http://www.slideshare.net/slidesharepython/python-slideshare-api-test-20130524t162943687234")
    # self.assertEqual(sls['Slideshow']['ID'], slideshow_id)


def test_get_slideshow_by_url_exclude_tags(client):
    pass


def test_get_slideshows_by_tag(client):
    tag = "crisis"
    response = client.slideshow.get_slideshows_by_tag(tag, limit=2)
    assert "Tag" in response
    assert "Count" in response["Tag"]
