from src.youtube_upload import build_video_resource


def test_youtube_resource_defaults_private():
    story = {
        "title": "اختبار خلف الرقم",
        "caption": "وصف قصير",
        "hashtags": ["AI", "السعودية"],
    }
    resource = build_video_resource(story)
    assert resource["status"]["privacyStatus"] == "private"
    assert resource["snippet"]["title"] == "اختبار خلف الرقم"
    assert "#AI" in resource["snippet"]["description"]
    assert resource["snippet"]["categoryId"] == "28"


def test_youtube_resource_normalizes_hashtags():
    resource = build_video_resource({"hashtags": ["#AI", "Tech"]})
    assert resource["snippet"]["tags"] == ["AI", "Tech"]
