import pytest

from galeriafora import ContentType


class TestContentType:
    def test_content_type_enum(self):
        assert ContentType.IMAGE_JPEG.value == "image/jpeg"
        assert ContentType.IMAGE_PNG.value == "image/png"
        assert ContentType.VIDEO_MP4.value == "video/mp4"
        assert ContentType.VIDEO_WEBM.value == "video/webm"
        assert ContentType.GIF.value == "image/gif"

    def test_str_representation(self):
        for content_type in ContentType.__members__.values():
            assert str(content_type) == content_type.value

    def test_equality(self):
        assert ContentType.IMAGE_JPEG == ContentType.IMAGE_JPEG
        assert ContentType.IMAGE_JPEG != ContentType.IMAGE_PNG
        assert ContentType.VIDEO_MP4 == ContentType.VIDEO_MP4
        assert ContentType.VIDEO_MP4 != ContentType.VIDEO_WEBM
        assert ContentType.GIF == ContentType.GIF
        assert ContentType.GIF != ContentType.IMAGE_JPEG

    def test_can_be_created_from_string(self):
        assert ContentType("image/jpeg") == ContentType.IMAGE_JPEG
        assert ContentType("image/png") == ContentType.IMAGE_PNG
        assert ContentType("video/mp4") == ContentType.VIDEO_MP4
        assert ContentType("video/webm") == ContentType.VIDEO_WEBM
        assert ContentType("image/gif") == ContentType.GIF

    def test_string_equality(self):
        assert ContentType.IMAGE_JPEG == "image/jpeg"
        assert ContentType.IMAGE_PNG == "image/png"
        assert ContentType.VIDEO_MP4 == "video/mp4"
        assert ContentType.VIDEO_WEBM == "video/webm"
        assert ContentType.GIF == "image/gif"

    def test_can_be_assimilated_from_string(self):
        class CustomClass:
            def __init__(self, content_type: ContentType):
                self.content_type = content_type

        custom_instance = CustomClass(content_type="image/jpeg")
        assert custom_instance.content_type == ContentType.IMAGE_JPEG

    def test_repr_returns_enum_value(self):
        content_type = ContentType.IMAGE_JPEG
        assert repr(content_type) == "image/jpeg"
