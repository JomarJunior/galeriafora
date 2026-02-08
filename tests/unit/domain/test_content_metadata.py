import pytest

from galeriafora import ContentMetadata, ContentType


class TestContentMetadata:
    def test_can_be_created_with_valid_data(self):
        content_metadata = ContentMetadata(
            content_type=ContentType.IMAGE_JPEG,
            dimensions={"width": 800, "height": 600},
            file_size_bytes=102400,
        )

        assert content_metadata.content_type == ContentType.IMAGE_JPEG
        assert content_metadata.dimensions == {"width": 800, "height": 600}
        assert content_metadata.file_size_bytes == 102400

    def test_str_representation(self):
        content_metadata = ContentMetadata(
            content_type=ContentType.IMAGE_PNG,
            dimensions={"width": 1024, "height": 768},
            file_size_bytes=204800,
        )
        expected_str = (
            "ContentMetadata(content_type=image/png, "
            "dimensions={'width': 1024, 'height': 768}, "
            "file_size_bytes=204800)"
        )
        assert str(content_metadata) == expected_str

    def test_repr_representation(self):
        content_metadata = ContentMetadata(
            content_type=ContentType.GIF,
            dimensions={"width": 500, "height": 500},
            file_size_bytes=51200,
        )
        expected_repr = (
            "ContentMetadata(content_type=image/gif, "
            "dimensions={'width': 500, 'height': 500}, "
            "file_size_bytes=51200)"
        )
        assert repr(content_metadata) == expected_repr

    def test_equality(self):
        content_metadata1 = ContentMetadata(
            content_type=ContentType.IMAGE_JPEG,
            dimensions={"width": 800, "height": 600},
            file_size_bytes=102400,
        )
        content_metadata2 = ContentMetadata(
            content_type=ContentType.IMAGE_JPEG,
            dimensions={"width": 800, "height": 600},
            file_size_bytes=102400,
        )
        content_metadata3 = ContentMetadata(
            content_type=ContentType.IMAGE_PNG,
            dimensions={"width": 1024, "height": 768},
            file_size_bytes=204800,
        )

        assert content_metadata1 == content_metadata2
        assert content_metadata1 != content_metadata3

    def test_immutability(self):
        content_metadata = ContentMetadata(
            content_type=ContentType.IMAGE_JPEG,
            dimensions={"width": 800, "height": 600},
            file_size_bytes=102400,
        )

        with pytest.raises(AttributeError):
            content_metadata.content_type = ContentType.IMAGE_PNG

        with pytest.raises(AttributeError):
            content_metadata.dimensions = {"width": 1024, "height": 768}

        with pytest.raises(AttributeError):
            content_metadata.file_size_bytes = 204800

    def test_serialization(self):
        content_metadata = ContentMetadata(
            content_type=ContentType.IMAGE_JPEG,
            dimensions={"width": 800, "height": 600},
            file_size_bytes=102400,
        )
        serialized = content_metadata.to_dict()
        assert serialized == {
            "content_type": "image/jpeg",
            "dimensions": {"width": 800, "height": 600},
            "file_size_bytes": 102400,
        }

    def test_deserialization(self):
        data = {
            "content_type": "image/png",
            "dimensions": {"width": 1024, "height": 768},
            "file_size_bytes": 204800,
        }
        content_metadata = ContentMetadata.from_dict(data)
        assert content_metadata.content_type == ContentType.IMAGE_PNG
        assert content_metadata.dimensions == {"width": 1024, "height": 768}
        assert content_metadata.file_size_bytes == 204800

    def test_has_correct_aspect_ratio_property(self):
        content_metadata = ContentMetadata(
            content_type=ContentType.IMAGE_JPEG,
            dimensions={"width": 800, "height": 600},
            file_size_bytes=102400,
        )
        assert content_metadata.aspect_ratio == 800 / 600

    def test_has_correct_is_portrait_property(self):
        content_metadata = ContentMetadata(
            content_type=ContentType.IMAGE_JPEG,
            dimensions={"width": 600, "height": 800},
            file_size_bytes=102400,
        )
        assert content_metadata.is_portrait is True

    def test_has_correct_is_landscape_property(self):
        content_metadata = ContentMetadata(
            content_type=ContentType.IMAGE_JPEG,
            dimensions={"width": 800, "height": 600},
            file_size_bytes=102400,
        )
        assert content_metadata.is_landscape is True

    def test_has_correct_is_square_property(self):
        content_metadata = ContentMetadata(
            content_type=ContentType.IMAGE_JPEG,
            dimensions={"width": 500, "height": 500},
            file_size_bytes=51200,
        )
        assert content_metadata.is_square is True

    def test_has_correct_file_size_kb_property(self):
        content_metadata = ContentMetadata(
            content_type=ContentType.IMAGE_JPEG,
            dimensions={"width": 800, "height": 600},
            file_size_bytes=102400,
        )
        assert content_metadata.file_size_kb == 102400 / 1024

    def test_has_correct_file_size_mb_property(self):
        content_metadata = ContentMetadata(
            content_type=ContentType.IMAGE_JPEG,
            dimensions={"width": 800, "height": 600},
            file_size_bytes=102400,
        )
        assert content_metadata.file_size_mb == 102400 / (1024 * 1024)

    def test_has_correct_file_extension_property(self):
        content_metadata = ContentMetadata(
            content_type=ContentType.IMAGE_JPEG,
            dimensions={"width": 800, "height": 600},
            file_size_bytes=102400,
        )
        assert content_metadata.file_extension == "jpg"
