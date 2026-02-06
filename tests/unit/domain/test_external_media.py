import pytest

from galeriafora import (
    AiMetadata,
    ContentMetadata,
    ContentType,
    ExternalMedia,
    ExternalProviderCapability,
    ExternalProviderInfo,
    ExternalProviderName,
    MatureRating,
)
from galeriafora.domain.exceptions import (
    CannotCreateExternalMediaWithDescriptionExceedingMaxLengthException,
    CannotCreateExternalMediaWithEmptyTitleException,
    CannotCreateExternalMediaWithInvalidContentMetadataException,
    CannotCreateExternalMediaWithInvalidProviderException,
    CannotCreateExternalMediaWithInvalidRatingException,
    CannotCreateExternalMediaWithInvalidURLException,
    CannotCreateExternalMediaWithTitleExceedingMaxLengthException,
    CannotCreateExternalMediaWithTooManyTagsException,
)


class TestExternalMedia:
    def test_can_be_created_with_valid_data(self):
        media = ExternalMedia(
            url="https://example.com/image.jpg",
            title="Example Image",
            description="An example image from an external provider.",
            content_metadata=ContentMetadata(
                content_type=ContentType.IMAGE_PNG,
                dimensions={"width": 800, "height": 600},
                file_size_bytes=150000,
            ),
            tags=["example", "test"],
            mature_rating=MatureRating.PG,
            ai_metadata=AiMetadata(is_ai_generated=False),
            provider=ExternalProviderInfo(
                name=ExternalProviderName("exampleprovider"),
                description="A test provider",
                capabilities=[
                    ExternalProviderCapability.FETCH_LATEST,
                ],
            ),
        )

        assert media.url == "https://example.com/image.jpg"
        assert media.title == "Example Image"
        assert media.description == "An example image from an external provider."
        assert media.content_metadata.content_type == ContentType.IMAGE_PNG
        assert media.content_metadata.dimensions == {"width": 800, "height": 600}
        assert media.content_metadata.file_size_bytes == 150000
        assert media.tags == ["example", "test"]
        assert media.mature_rating == MatureRating.PG
        assert media.ai_metadata == AiMetadata(is_ai_generated=False)
        assert media.provider.name == ExternalProviderName("exampleprovider")
        assert media.provider.description == "A test provider"
        assert media.provider.capabilities == [ExternalProviderCapability.FETCH_LATEST]

    def test_creation_with_invalid_url_should_raise_error(self):
        with pytest.raises(CannotCreateExternalMediaWithInvalidURLException):
            ExternalMedia(
                url="invalid-url",
                title="Invalid URL Media",
                description="This media has an invalid URL.",
                content_metadata=ContentMetadata(
                    content_type=ContentType.IMAGE_JPEG,
                    dimensions={"width": 640, "height": 480},
                    file_size_bytes=120000,
                ),
                tags=["invalid", "test"],
                mature_rating=MatureRating.PG,
                ai_metadata=None,
                provider=ExternalProviderInfo(
                    name=ExternalProviderName("testprovider"),
                    description="A test provider",
                    capabilities=[
                        ExternalProviderCapability.FETCH_LATEST,
                    ],
                ),
            )

    def test_creation_with_http_url(self):
        media = ExternalMedia(
            url="http://example.com/video.mp4",
            title="HTTP Video",
            description="A video from HTTP URL.",
            content_metadata=ContentMetadata(
                content_type=ContentType.VIDEO_MP4,
                dimensions={"width": 1920, "height": 1080},
                file_size_bytes=5000000,
            ),
            tags=["http", "video"],
            mature_rating=MatureRating.R,
            ai_metadata={"generated": True},
            provider=ExternalProviderInfo(
                name=ExternalProviderName("httpprovider"),
                description="HTTP provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST, ExternalProviderCapability.SEARCH],
            ),
        )
        assert media.url == "http://example.com/video.mp4"
        assert media.content_metadata.content_type == ContentType.VIDEO_MP4
        assert media.mature_rating == MatureRating.R
        assert media.ai_metadata == {"generated": True}
        assert ExternalProviderCapability.SEARCH in media.provider.capabilities

    def test_creation_with_empty_tags(self):
        media = ExternalMedia(
            url="https://example.com/audio.wav",
            title="Audio File",
            description="An audio file.",
            content_metadata=ContentMetadata(
                content_type=ContentType.AUDIO_WAV,
                dimensions=None,
                file_size_bytes=2000000,
            ),
            tags=[],
            mature_rating=MatureRating.PG,
            ai_metadata=None,
            provider=ExternalProviderInfo(
                name=ExternalProviderName("audioprovider"),
                description="Audio provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        assert media.tags == []

    def test_creation_with_special_characters_in_title_and_description(self):
        media = ExternalMedia(
            url="https://example.com/image.png",
            title="Title with émojis 🖼️ and symbols @#$%",
            description="Description with accents: naïve café.",
            content_metadata=ContentMetadata(
                content_type=ContentType.IMAGE_PNG,
                dimensions={"width": 1024, "height": 768},
                file_size_bytes=300000,
            ),
            tags=["special", "chars"],
            mature_rating=MatureRating.PG_13,
            ai_metadata=None,
            provider=ExternalProviderInfo(
                name=ExternalProviderName("specialprovider"),
                description="Provider with specials",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        assert "émojis" in media.title
        assert "naïve" in media.description

    def test_creation_with_zero_dimensions(self):
        media = ExternalMedia(
            url="https://example.com/image.gif",
            title="Zero Dim Image",
            description="Image with zero dimensions.",
            content_metadata=ContentMetadata(
                content_type=ContentType.IMAGE_GIF,
                dimensions={"width": 0, "height": 0},
                file_size_bytes=1000,
            ),
            tags=["zero"],
            mature_rating=MatureRating.XXX,
            ai_metadata=None,
            provider=ExternalProviderInfo(
                name=ExternalProviderName("zeroprovider"),
                description="Zero provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        assert media.content_metadata.dimensions == {"width": 0, "height": 0}

    def test_creation_with_large_file_size(self):
        media = ExternalMedia(
            url="https://example.com/large.mp4",
            title="Large Video",
            description="Very large video file.",
            content_metadata=ContentMetadata(
                content_type=ContentType.VIDEO_MP4,
                dimensions={"width": 3840, "height": 2160},
                file_size_bytes=10000000000,  # 10GB
            ),
            tags=["large", "4k"],
            mature_rating=MatureRating.PG,
            ai_metadata={"resolution": "4K"},
            provider=ExternalProviderInfo(
                name=ExternalProviderName("largeprovider"),
                description="Large file provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        assert media.content_metadata.file_size_bytes == 10000000000

    def test_creation_with_invalid_content_type_should_raise_error(self):
        with pytest.raises(CannotCreateExternalMediaWithInvalidContentMetadataException):
            ExternalMedia(
                url="https://example.com/invalid.txt",
                title="Invalid Content",
                description="Invalid content type.",
                content_metadata=ContentMetadata(
                    content_type="INVALID_TYPE",  # Assuming invalid type
                    dimensions={"width": 100, "height": 100},
                    file_size_bytes=50000,
                ),
                tags=["invalid"],
                mature_rating=MatureRating.PG,
                ai_metadata=None,
                provider=ExternalProviderInfo(
                    name=ExternalProviderName("invalidprovider"),
                    description="Invalid provider",
                    capabilities=[ExternalProviderCapability.FETCH_LATEST],
                ),
            )

    def test_creation_with_negative_file_size_should_raise_error(self):
        with pytest.raises(CannotCreateExternalMediaWithInvalidContentMetadataException):
            ExternalMedia(
                url="https://example.com/negative.mp3",
                title="Negative Size",
                description="Negative file size.",
                content_metadata=ContentMetadata(
                    content_type=ContentType.AUDIO_MP3,
                    dimensions=None,
                    file_size_bytes=-1000,
                ),
                tags=["negative"],
                mature_rating=MatureRating.PG,
                ai_metadata=None,
                provider=ExternalProviderInfo(
                    name=ExternalProviderName("negativeprovider"),
                    description="Negative provider",
                    capabilities=[ExternalProviderCapability.FETCH_LATEST],
                ),
            )

    def test_creation_with_invalid_rating_should_raise_error(self):
        with pytest.raises(CannotCreateExternalMediaWithInvalidRatingException):
            ExternalMedia(
                url="https://example.com/invalid_rating.jpg",
                title="Invalid Rating",
                description="Invalid rating.",
                content_metadata=ContentMetadata(
                    content_type=ContentType.IMAGE_JPEG,
                    dimensions={"width": 800, "height": 600},
                    file_size_bytes=150000,
                ),
                tags=["invalid"],
                mature_rating="INVALID_RATING",  # Assuming invalid rating
                ai_metadata=None,
                provider=ExternalProviderInfo(
                    name=ExternalProviderName("ratingprovider"),
                    description="Rating provider",
                    capabilities=[ExternalProviderCapability.FETCH_LATEST],
                ),
            )

    def test_creation_with_empty_title_should_raise_error(self):
        with pytest.raises(CannotCreateExternalMediaWithEmptyTitleException):
            ExternalMedia(
                url="https://example.com/empty_title.png",
                title="",
                description="Empty title.",
                content_metadata=ContentMetadata(
                    content_type=ContentType.IMAGE_PNG,
                    dimensions={"width": 640, "height": 480},
                    file_size_bytes=120000,
                ),
                tags=["empty"],
                mature_rating=MatureRating.PG,
                ai_metadata=None,
                provider=ExternalProviderInfo(
                    name=ExternalProviderName("emptyprovider"),
                    description="Empty provider",
                    capabilities=[ExternalProviderCapability.FETCH_LATEST],
                ),
            )

    def test_creation_with_none_provider_should_raise_error(self):
        with pytest.raises(CannotCreateExternalMediaWithInvalidProviderException):
            ExternalMedia(
                url="https://example.com/no_provider.jpg",
                title="No Provider",
                description="No provider info.",
                content_metadata=ContentMetadata(
                    content_type=ContentType.IMAGE_JPEG,
                    dimensions={"width": 800, "height": 600},
                    file_size_bytes=150000,
                ),
                tags=["no_provider"],
                mature_rating=MatureRating.PG,
                ai_metadata=None,
                provider=None,
            )

    def test_creation_with_url_containing_spaces_should_raise_error(self):
        with pytest.raises(CannotCreateExternalMediaWithInvalidURLException):
            ExternalMedia(
                url="https://example.com/image with spaces.jpg",
                title="Spaces in URL",
                description="URL with spaces.",
                content_metadata=ContentMetadata(
                    content_type=ContentType.IMAGE_JPEG,
                    dimensions={"width": 640, "height": 480},
                    file_size_bytes=120000,
                ),
                tags=["spaces"],
                mature_rating=MatureRating.PG,
                ai_metadata=None,
                provider=ExternalProviderInfo(
                    name=ExternalProviderName("spacesprovider"),
                    description="Spaces provider",
                    capabilities=[ExternalProviderCapability.FETCH_LATEST],
                ),
            )

    def test_creation_with_title_with_only_whitespace_should_raise_error(self):
        with pytest.raises(CannotCreateExternalMediaWithEmptyTitleException):
            ExternalMedia(
                url="https://example.com/whitespace_title.jpg",
                title="   ",
                description="Title with only whitespace.",
                content_metadata=ContentMetadata(
                    content_type=ContentType.IMAGE_JPEG,
                    dimensions={"width": 800, "height": 600},
                    file_size_bytes=150000,
                ),
                tags=["whitespace"],
                mature_rating=MatureRating.PG,
                ai_metadata=None,
                provider=ExternalProviderInfo(
                    name=ExternalProviderName("whitespaceprovider"),
                    description="Whitespace provider",
                    capabilities=[ExternalProviderCapability.FETCH_LATEST],
                ),
            )

    def test_creation_with_title_exceeding_max_length_should_raise_error(self):
        long_title = "A" * 256  # Assuming max length is 255 characters
        with pytest.raises(CannotCreateExternalMediaWithTitleExceedingMaxLengthException):
            ExternalMedia(
                url="https://example.com/long_title.jpg",
                title=long_title,
                description="Title exceeding max length.",
                content_metadata=ContentMetadata(
                    content_type=ContentType.IMAGE_JPEG,
                    dimensions={"width": 800, "height": 600},
                    file_size_bytes=150000,
                ),
                tags=["long_title"],
                mature_rating=MatureRating.PG,
                ai_metadata=None,
                provider=ExternalProviderInfo(
                    name=ExternalProviderName("longtitleprovider"),
                    description="Long title provider",
                    capabilities=[ExternalProviderCapability.FETCH_LATEST],
                ),
            )

    def test_creation_with_description_exceeding_max_length_should_raise_error(self):
        long_description = "D" * 2049  # Assuming max length is 2048 characters
        with pytest.raises(CannotCreateExternalMediaWithDescriptionExceedingMaxLengthException):
            ExternalMedia(
                url="https://example.com/long_description.jpg",
                title="Long Description",
                description=long_description,
                content_metadata=ContentMetadata(
                    content_type=ContentType.IMAGE_JPEG,
                    dimensions={"width": 800, "height": 600},
                    file_size_bytes=150000,
                ),
                tags=["long_description"],
                mature_rating=MatureRating.PG,
                ai_metadata=None,
                provider=ExternalProviderInfo(
                    name=ExternalProviderName("longdescriptionprovider"),
                    description="Long description provider",
                    capabilities=[ExternalProviderCapability.FETCH_LATEST],
                ),
            )

    def test_creation_with_too_many_tags_should_raise_error(self):
        tags = [f"tag{i}" for i in range(31)]  # Assuming max tags is 30
        with pytest.raises(CannotCreateExternalMediaWithTooManyTagsException):
            ExternalMedia(
                url="https://example.com/too_many_tags.jpg",
                title="Too Many Tags",
                description="This media has too many tags.",
                content_metadata=ContentMetadata(
                    content_type=ContentType.IMAGE_JPEG,
                    dimensions={"width": 800, "height": 600},
                    file_size_bytes=150000,
                ),
                tags=tags,
                mature_rating=MatureRating.PG,
                ai_metadata=None,
                provider=ExternalProviderInfo(
                    name=ExternalProviderName("toomanytagsprovider"),
                    description="Too many tags provider",
                    capabilities=[ExternalProviderCapability.FETCH_LATEST],
                ),
            )

    def test_can_be_created_with_null_ai_metadata(self):
        media = ExternalMedia(
            url="https://example.com/null_ai.jpg",
            title="Null AI Metadata",
            description="Media with null AI metadata.",
            content_metadata=ContentMetadata(
                content_type=ContentType.IMAGE_JPEG,
                dimensions={"width": 800, "height": 600},
                file_size_bytes=150000,
            ),
            tags=["null_ai"],
            mature_rating=MatureRating.PG,
            ai_metadata=None,
            provider=ExternalProviderInfo(
                name=ExternalProviderName("nullaiprovider"),
                description="Null AI provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        assert media.ai_metadata is None

    def test_can_be_created_with_ai_metadata(self):
        media = ExternalMedia(
            url="https://example.com/with_ai.jpg",
            title="With AI Metadata",
            description="Media with AI metadata.",
            content_metadata=ContentMetadata(
                content_type=ContentType.IMAGE_JPEG,
                dimensions={"width": 800, "height": 600},
                file_size_bytes=150000,
            ),
            tags=["with_ai"],
            mature_rating=MatureRating.PG,
            ai_metadata=AiMetadata(is_ai_generated=False),
            provider=ExternalProviderInfo(
                name=ExternalProviderName("withaiprovider"),
                description="With AI provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        assert media.ai_metadata == AiMetadata(is_ai_generated=False)

    def test_can_be_serialized_to_dict(self):
        media = ExternalMedia(
            url="https://example.com/serialize.jpg",
            title="Serialize Test",
            description="Testing serialization to dict.",
            content_metadata=ContentMetadata(
                content_type=ContentType.IMAGE_JPEG,
                dimensions={"width": 800, "height": 600},
                file_size_bytes=150000,
            ),
            tags=["serialize", "test"],
            mature_rating=MatureRating.PG,
            ai_metadata=AiMetadata(is_ai_generated=False),
            provider=ExternalProviderInfo(
                name=ExternalProviderName("serializeprovider"),
                description="Serialize provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        media_dict = media.to_dict()
        assert media_dict["url"] == "https://example.com/serialize.jpg"
        assert media_dict["title"] == "Serialize Test"
        assert media_dict["description"] == "Testing serialization to dict."
        assert media_dict["content_metadata"]["content_type"] == "IMAGE_JPEG"
        assert media_dict["content_metadata"]["dimensions"] == {"width": 800, "height": 600}
        assert media_dict["content_metadata"]["file_size_bytes"] == 150000
        assert media_dict["tags"] == ["serialize", "test"]
        assert media_dict["mature_rating"] == "PG"
        assert media_dict["ai_metadata"] == {"is_ai_generated": False}
        assert media_dict["provider"]["name"] == "serializeprovider"
        assert media_dict["provider"]["description"] == "Serialize provider"
        assert media_dict["provider"]["capabilities"] == ["FETCH_LATEST"]

    def test_can_be_deserialized_from_dict(self):
        media_data = {
            "url": "https://example.com/deserialize.jpg",
            "title": "Deserialize Test",
            "description": "Testing deserialization from dict.",
            "content_metadata": {
                "content_type": "IMAGE_JPEG",
                "dimensions": {"width": 800, "height": 600},
                "file_size_bytes": 150000,
            },
            "tags": ["deserialize", "test"],
            "mature_rating": "PG",
            "ai_metadata": {"is_ai_generated": False},
            "provider": {
                "name": "deserializeprovider",
                "description": "Deserialize provider",
                "capabilities": ["FETCH_LATEST"],
            },
        }
        media = ExternalMedia.from_dict(media_data)
        assert media.url == "https://example.com/deserialize.jpg"
        assert media.title == "Deserialize Test"
        assert media.description == "Testing deserialization from dict."
        assert media.content_metadata.content_type == ContentType.IMAGE_JPEG
        assert media.content_metadata.dimensions == {"width": 800, "height": 600}
        assert media.content_metadata.file_size_bytes == 150000
        assert media.tags == ["deserialize", "test"]
        assert media.mature_rating == MatureRating.PG
        assert media.ai_metadata == AiMetadata(is_ai_generated=False)
        assert media.provider.name == ExternalProviderName("deserializeprovider")
        assert media.provider.description == "Deserialize provider"
        assert media.provider.capabilities == [ExternalProviderCapability.FETCH_LATEST]

    def test_equality(self):
        media1 = ExternalMedia(
            url="https://example.com/equality.jpg",
            title="Equality Test",
            description="Testing equality.",
            content_metadata=ContentMetadata(
                content_type=ContentType.IMAGE_JPEG,
                dimensions={"width": 800, "height": 600},
                file_size_bytes=150000,
            ),
            tags=["equality", "test"],
            mature_rating=MatureRating.PG,
            ai_metadata=AiMetadata(is_ai_generated=False),
            provider=ExternalProviderInfo(
                name=ExternalProviderName("equalityprovider"),
                description="Equality provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        media2 = ExternalMedia(
            url="https://example.com/equality.jpg",
            title="Equality Test",
            description="Testing equality.",
            content_metadata=ContentMetadata(
                content_type=ContentType.IMAGE_JPEG,
                dimensions={"width": 800, "height": 600},
                file_size_bytes=150000,
            ),
            tags=["equality", "test"],
            mature_rating=MatureRating.PG,
            ai_metadata=AiMetadata(is_ai_generated=False),
            provider=ExternalProviderInfo(
                name=ExternalProviderName("equalityprovider"),
                description="Equality provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        media3 = ExternalMedia(
            url="https://example.com/different.jpg",
            title="Different Media",
            description="This media is different.",
            content_metadata=ContentMetadata(
                content_type=ContentType.IMAGE_PNG,
                dimensions={"width": 1024, "height": 768},
                file_size_bytes=200000,
            ),
            tags=["different"],
            mature_rating=MatureRating.R,
            ai_metadata=None,
            provider=ExternalProviderInfo(
                name=ExternalProviderName("differentprovider"),
                description="Different provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        assert media1 == media2
        assert media1 != media3

    def test_immutability(self):
        media = ExternalMedia(
            url="https://example.com/immutable.jpg",
            title="Immutable Test",
            description="Testing immutability.",
            content_metadata=ContentMetadata(
                content_type=ContentType.IMAGE_JPEG,
                dimensions={"width": 800, "height": 600},
                file_size_bytes=150000,
            ),
            tags=["immutable", "test"],
            mature_rating=MatureRating.PG,
            ai_metadata=AiMetadata(is_ai_generated=False),
            provider=ExternalProviderInfo(
                name=ExternalProviderName("immutableprovider"),
                description="Immutable provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        with pytest.raises(AttributeError):
            media.url = "https://example.com/changed.jpg"
        with pytest.raises(AttributeError):
            media.title = "Changed Title"
        with pytest.raises(AttributeError):
            media.description = "Changed Description"
        with pytest.raises(AttributeError):
            media.content_metadata = ContentMetadata(
                content_type=ContentType.IMAGE_PNG,
                dimensions={"width": 1024, "height": 768},
                file_size_bytes=200000,
            )
        with pytest.raises(AttributeError):
            media.tags.append("new_tag")
        with pytest.raises(AttributeError):
            media.mature_rating = MatureRating.R
        with pytest.raises(AttributeError):
            media.ai_metadata = AiMetadata(is_ai_generated=True)
        with pytest.raises(AttributeError):
            media.provider = ExternalProviderInfo(
                name=ExternalProviderName("changedprovider"),
                description="Changed provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            )

    def test_str_representation(self):
        media = ExternalMedia(
            url="https://example.com/str.jpg",
            title="String Representation",
            description="Testing __str__ method.",
            content_metadata=ContentMetadata(
                content_type=ContentType.IMAGE_JPEG,
                dimensions={"width": 800, "height": 600},
                file_size_bytes=150000,
            ),
            tags=["string", "test"],
            mature_rating=MatureRating.PG,
            ai_metadata=AiMetadata(is_ai_generated=False),
            provider=ExternalProviderInfo(
                name=ExternalProviderName("strprovider"),
                description="String provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        expected_str = (
            "ExternalMedia(url='https://example.com/str.jpg', title='String Representation', "
            "description='Testing __str__ method.', content_metadata=ContentMetadata(content_type=ContentType.IMAGE_JPEG, "
            "dimensions={'width': 800, 'height': 600}, file_size_bytes=150000), tags=['string', 'test'], "
            "mature_rating='pg', ai_metadata=AiMetadata(is_ai_generated=False), provider=ExternalProviderInfo(name=ExternalProviderName('strprovider'), "
            "description='String provider', capabilities=[<ExternalProviderCapability.FETCH_LATEST: 'FETCH_LATEST'>]))"
        )
        assert str(media) == expected_str

    def test_repr_representation(self):
        media = ExternalMedia(
            url="https://example.com/repr.jpg",
            title="Repr Representation",
            description="Testing __repr__ method.",
            content_metadata=ContentMetadata(
                content_type=ContentType.IMAGE_JPEG,
                dimensions={"width": 800, "height": 600},
                file_size_bytes=150000,
            ),
            tags=["repr", "test"],
            mature_rating=MatureRating.PG,
            ai_metadata=AiMetadata(is_ai_generated=False),
            provider=ExternalProviderInfo(
                name=ExternalProviderName("reprprovider"),
                description="Repr provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        expected_repr = (
            "ExternalMedia(url='https://example.com/repr.jpg', title='Repr Representation', "
            "description='Testing __repr__ method.', content_metadata=ContentMetadata(content_type=ContentType.IMAGE_JPEG, "
            "dimensions={'width': 800, 'height': 600}, file_size_bytes=150000), tags=['repr', 'test'], "
            "mature_rating='pg', ai_metadata=AiMetadata(is_ai_generated=False), provider=ExternalProviderInfo(name=ExternalProviderName('reprprovider'), "
            "description='Repr provider', capabilities=[<ExternalProviderCapability.FETCH_LATEST: 'FETCH_LATEST'>]))"
        )
        assert repr(media) == expected_repr

    def test_is_hashable(self):
        media = ExternalMedia(
            url="https://example.com/hashable.jpg",
            title="Hashable Test",
            description="Testing hashability.",
            content_metadata=ContentMetadata(
                content_type=ContentType.IMAGE_JPEG,
                dimensions={"width": 800, "height": 600},
                file_size_bytes=150000,
            ),
            tags=["hashable", "test"],
            mature_rating=MatureRating.PG,
            ai_metadata=AiMetadata(is_ai_generated=False),
            provider=ExternalProviderInfo(
                name=ExternalProviderName("hashableprovider"),
                description="Hashable provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        assert isinstance(hash(media), int)

    def test_can_be_key_in_dict(self):
        media = ExternalMedia(
            url="https://example.com/dict_key.jpg",
            title="Dict Key Test",
            description="Testing if ExternalMedia can be a dict key.",
            content_metadata=ContentMetadata(
                content_type=ContentType.IMAGE_JPEG,
                dimensions={"width": 800, "height": 600},
                file_size_bytes=150000,
            ),
            tags=["dict_key", "test"],
            mature_rating=MatureRating.PG,
            ai_metadata=AiMetadata(is_ai_generated=False),
            provider=ExternalProviderInfo(
                name=ExternalProviderName("dictkeyprovider"),
                description="Dict key provider",
                capabilities=[ExternalProviderCapability.FETCH_LATEST],
            ),
        )
        media_dict = {media: "This is a value associated with the ExternalMedia key."}
        assert media in media_dict
        assert media_dict[media] == "This is a value associated with the ExternalMedia key."
