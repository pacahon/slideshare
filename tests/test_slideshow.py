import pytest

def test_get_slideshow_by_id(client, slideshow):
    response = client.get_slideshow(slideshow_id=slideshow.id)
    assert "Slideshow" in response
    assert response['Slideshow']['ID'] == slideshow.id
    assert response['Slideshow']['URL'] == slideshow.url
    assert "Tags" not in response['Slideshow']

def test_get_slideshow_by_url(client, slideshow):
    response = client.get_slideshow(slideshow_url=slideshow.url)
    assert "Slideshow" in response
    assert response['Slideshow']['ID'] == slideshow.id

def test_get_slideshow_combined(client, slideshow):
    """Make sure slideshow_id has precedence over slideshow_url"""
    response = client.get_slideshow(slideshow_id=slideshow.id,
                                    slideshow_url="dummy_url")
    assert response['Slideshow']['URL'] == slideshow.url

def test_get_slideshow_by_id_with_detail(client, slideshow):
    response = client.get_slideshow(slideshow_id=slideshow.id, detailed=True)
    assert "Tags" in response['Slideshow']

@pytest.mark.skipif(True, reason="No idea is it really usefull for anybody")
def test_get_slideshow_by_url_exclude_tags(client):
    pass

def test_get_slideshow_by_id_with_transcript(client, slideshow):
    response = client.get_slideshow(slideshow_id=slideshow.id, get_transcript=True)
    assert "Transcript" in response["Slideshow"]

def test_get_slideshows_by_tag(client):
    super_popular_tag = "slideshare"
    response = client.get_slideshows_by_tag(super_popular_tag, limit=2)
    assert "Tag" in response
    assert "Count" in response["Tag"]
    assert "Slideshow" in response["Tag"]
    assert len(response["Tag"]["Slideshow"]) == 2

def test_get_slideshows_by_tag_limit(client):
    super_popular_tag = "slideshare"
    response = client.get_slideshows_by_tag(super_popular_tag, limit=1)
    assert "Tag" in response
    assert "Slideshow" in response["Tag"]
    assert isinstance(response["Tag"]["Slideshow"], dict)
    response = client.get_slideshows_by_tag(super_popular_tag, limit=2)
    assert isinstance(response["Tag"]["Slideshow"], list)

def test_get_slideshows_by_tag_detailed(client):
    super_popular_tag = "slideshare"
    response = client.get_slideshows_by_tag(super_popular_tag, limit=1, detailed=True)
    assert "Tag" in response
    assert "Slideshow" in response["Tag"]
    assert "Tags" in response["Tag"]["Slideshow"]

def test_get_slideshows_by_tag_offset(client):
    super_popular_tag = "slideshare"
    response = client.get_slideshows_by_tag(super_popular_tag, limit=2)
    assert "Tag" in response
    assert "Count" in response["Tag"]
    assert int(response["Tag"]["Count"]) > 2
    assert "Slideshow" in response["Tag"]
    assert len(response["Tag"]["Slideshow"]) == 2
    slideshow_id = response["Tag"]["Slideshow"][1]["ID"]
    response = client.get_slideshows_by_tag(super_popular_tag, limit=2, offset=1)
    assert response["Tag"]["Slideshow"][0]["ID"] == slideshow_id


def test_upload_slideshow_by_upload_url(client):
    upload_url = "https://github.com/pacahon/slideshare/raw/master/tests/test_slideshow/slide.pdf"
    slideshow_title = "Test Slideshow Title"
    description = "Slideshow Description"
    tags = ["test1", "test2"]

    response = client.upload_slideshow(slideshow_title,
                                       upload_url=upload_url,
                                       slideshow_description=description,
                                       slideshow_tags=tags
                                       )
    assert "SlideShowUploaded" in response
    assert "SlideShowID" in response["SlideShowUploaded"]
    slideshow_id = response["SlideShowUploaded"]["SlideShowID"]
    response = client.get_slideshow(slideshow_id=slideshow_id, detailed=True)
    assert "Slideshow" in response
    assert response["Slideshow"]["Description"] == description
    assert all(tag in tags for tag in
               (tag["#text"] for tag in response["Slideshow"]["Tags"]["Tag"]))
    response = client.delete_slideshow(slideshow_id=slideshow_id)
    assert "SlideShowDeleted" in response
    assert response['SlideShowDeleted']['SlideshowID'] == slideshow_id


def test_upload_slideshow_by_slideshow_srcfile(client, datadir):
    slideshow_title = "Test Slideshow Title"
    slideshow_srcfile = datadir.join("test.odp").strpath
    response = client.upload_slideshow(slideshow_title,
                                       slideshow_srcfile=slideshow_srcfile)
    assert "SlideShowUploaded" in response
    assert "SlideShowID" in response["SlideShowUploaded"]
    slideshow_id = response["SlideShowUploaded"]["SlideShowID"]
    response = client.delete_slideshow(slideshow_id=slideshow_id)
    assert "SlideShowDeleted" in response
    assert response['SlideShowDeleted']['SlideshowID'] == slideshow_id


# TODO: Test upload big files
# TODO: Think about upload limitations