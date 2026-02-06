"""
Unit tests for MediaUploader application service.

This test suite validates the MediaUploader's orchestration logic, ensuring proper
coordination with the ProviderRegistry and IExternalProvider interface according to
hexagonal architecture principles.

Tests use unittest.mock for creating test doubles and verifying interactions.
"""

from typing import Dict, List, Optional, Sequence
from unittest.mock import AsyncMock, Mock, create_autospec

import pytest

from galeriafora import (
    AiMetadata,
    ContentMetadata,
    ContentType,
    ExternalMedia,
    ExternalProviderCapability,
    ExternalProviderInfo,
    ExternalProviderName,
    IExternalProvider,
    MatureRating,
    MediaUploader,
    ProviderRegistry,
)
from galeriafora.domain.exceptions import (
    CannotInitializeMediaUploaderWithInvalidProviderRegistryException,
    CannotUploadMediaProviderDoesNotSupportUploadException,
    CannotUploadMediaToMultipleWithInvalidProviderNameException,
    CannotUploadMediaToMultipleWithoutRegisteredProvidersException,
    CannotUploadMediaWithInvalidProviderNameException,
    CannotUploadMediaWithoutRegisteredProvidersException,
)

# Constants following architecture documentation
TEST_MEDIA_URL = "https://example.com/test_media.jpg"
TEST_MEDIA_TITLE = "Test Media"


# Helper functions for creating test data
def create_test_media(
    url: str = TEST_MEDIA_URL,
    title: str = TEST_MEDIA_TITLE,
    description: str = "Test media description",
    tags: Optional[List[str]] = None,
    provider_name: str = "mockprovider",
) -> ExternalMedia:
    """Helper function to create test media items with consistent structure."""
    if tags is None:
        tags = ["test", "media"]

    return ExternalMedia(
        url=url,
        title=title,
        description=description,
        content_metadata=ContentMetadata(
            content_type=ContentType.IMAGE_JPEG,
            dimensions={"width": 800, "height": 600},
            file_size_bytes=150000,
        ),
        tags=tags,
        mature_rating=MatureRating.PG,
        ai_metadata=AiMetadata(is_ai_generated=False),
        provider=ExternalProviderInfo(
            name=ExternalProviderName(provider_name),
            description="A mock provider for testing.",
            capabilities=[
                ExternalProviderCapability.FETCH_LATEST,
                ExternalProviderCapability.FETCH_BY_USER,
                ExternalProviderCapability.FETCH_BY_TAGS,
                ExternalProviderCapability.UPLOAD,
            ],
        ),
    )


def create_mock_provider(name: str = "mockprovider") -> Mock:
    """Create a mock IExternalProvider using unittest.mock."""
    mock_provider = Mock(spec=IExternalProvider)

    # Set up provider info property
    mock_provider.info = ExternalProviderInfo(
        name=ExternalProviderName(name),
        description="A mock provider for testing.",
        capabilities=[
            ExternalProviderCapability.FETCH_LATEST,
            ExternalProviderCapability.FETCH_BY_USER,
            ExternalProviderCapability.FETCH_BY_TAGS,
            ExternalProviderCapability.UPLOAD,
        ],
    )

    # Mock async methods with AsyncMock
    mock_provider.fetch_latest = AsyncMock()
    mock_provider.fetch_by_user = AsyncMock()
    mock_provider.fetch_by_tags = AsyncMock()
    mock_provider.upload = AsyncMock()

    return mock_provider


def create_mock_provider_without_upload(name: str = "nouploadprovider") -> Mock:
    """Create a mock IExternalProvider without upload capability."""
    mock_provider = Mock(spec=IExternalProvider)

    # Set up provider info property without UPLOAD capability
    mock_provider.info = ExternalProviderInfo(
        name=ExternalProviderName(name),
        description="A mock provider without upload capability.",
        capabilities=[
            ExternalProviderCapability.FETCH_LATEST,
            ExternalProviderCapability.FETCH_BY_USER,
            ExternalProviderCapability.FETCH_BY_TAGS,
        ],
    )

    # Mock async methods with AsyncMock
    mock_provider.fetch_latest = AsyncMock()
    mock_provider.fetch_by_user = AsyncMock()
    mock_provider.fetch_by_tags = AsyncMock()
    # No upload method

    return mock_provider


def create_mock_registry(providers: list) -> Mock:
    """Create a mock ProviderRegistry using unittest.mock."""
    mock_registry = Mock(spec=ProviderRegistry)
    mock_registry.get_providers.return_value = providers
    return mock_registry


@pytest.fixture
def mock_provider() -> Mock:
    """Fixture providing a single mock provider with upload capability."""
    return create_mock_provider()


@pytest.fixture
def mock_provider_without_upload() -> Mock:
    """Fixture providing a mock provider without upload capability."""
    return create_mock_provider_without_upload()


@pytest.fixture
def mock_provider_registry(mock_provider) -> Mock:
    """Fixture providing a mock registry with a single provider."""
    return create_mock_registry([mock_provider])


@pytest.fixture
def single_provider_media_uploader(mock_provider_registry) -> MediaUploader:
    """Fixture providing a MediaUploader with a single mock provider."""
    return MediaUploader(provider_registry=mock_provider_registry)


@pytest.fixture
def multiple_providers_media_uploader() -> MediaUploader:
    """Fixture providing a MediaUploader with multiple mock providers."""
    provider1 = create_mock_provider("mockprovider")
    provider2 = create_mock_provider("mockprovider2")
    registry = create_mock_registry([provider1, provider2])
    return MediaUploader(provider_registry=registry)


@pytest.fixture
def empty_provider_media_uploader() -> MediaUploader:
    """Fixture providing a MediaUploader with no registered providers."""
    registry = create_mock_registry([])
    return MediaUploader(provider_registry=registry)


@pytest.fixture
def test_media() -> ExternalMedia:
    """Fixture providing test media for upload."""
    return create_test_media()


class TestMediaUploaderInitialization:
    """Test suite for MediaUploader initialization."""

    def test_initialization_with_single_provider(self, single_provider_media_uploader: MediaUploader, mock_provider):
        """Should successfully initialize MediaUploader with a single provider."""
        assert isinstance(single_provider_media_uploader, MediaUploader)
        providers = single_provider_media_uploader.provider_registry.get_providers()
        assert len(providers) == 1
        assert providers[0].info.name == "mockprovider"

    def test_initialization_with_multiple_providers(self, multiple_providers_media_uploader: MediaUploader):
        """Should successfully initialize MediaUploader with multiple providers."""
        assert isinstance(multiple_providers_media_uploader, MediaUploader)
        providers = multiple_providers_media_uploader.provider_registry.get_providers()
        assert len(providers) == 2
        provider_names = [provider.info.name for provider in providers]
        assert "mockprovider" in provider_names
        assert "mockprovider2" in provider_names

    def test_initialization_with_no_providers(self, empty_provider_media_uploader: MediaUploader):
        """Should successfully initialize MediaUploader even with no providers."""
        assert isinstance(empty_provider_media_uploader, MediaUploader)
        assert len(empty_provider_media_uploader.provider_registry.get_providers()) == 0

    @pytest.mark.parametrize(
        "invalid_registry",
        [
            "not a registry",
            123,
            [],
            {},
        ],
        ids=["string", "integer", "list", "dict"],
    )
    def test_initialization_with_invalid_provider_registry_should_raise_error(self, invalid_registry):
        """Should raise exception when initializing with invalid provider registry types."""
        with pytest.raises(CannotInitializeMediaUploaderWithInvalidProviderRegistryException):
            MediaUploader(provider_registry=invalid_registry)

    def test_initialization_with_none_provider_registry_should_raise_error(self):
        """Should raise exception when initializing with None as provider registry."""
        with pytest.raises(CannotInitializeMediaUploaderWithInvalidProviderRegistryException):
            MediaUploader(provider_registry=None)


class TestMediaUploaderUpload:
    """Test suite for MediaUploader.upload() method."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "invalid_provider_name",
        ["nonexistentprovider", None, ""],
        ids=["nonexistent", "none", "empty"],
    )
    async def test_upload_with_invalid_provider_name_should_raise_error(
        self, single_provider_media_uploader: MediaUploader, test_media: ExternalMedia, invalid_provider_name
    ):
        """Should raise exception when uploading with invalid provider names."""
        with pytest.raises(CannotUploadMediaWithInvalidProviderNameException):
            await single_provider_media_uploader.upload(provider_name=invalid_provider_name, media=test_media)

    @pytest.mark.asyncio
    async def test_upload_with_provider_that_does_not_support_upload_should_raise_error(
        self, test_media: ExternalMedia
    ):
        """Should raise exception when provider does not support upload capability."""
        # Arrange
        no_upload_provider = create_mock_provider_without_upload("noupload")
        registry = create_mock_registry([no_upload_provider])
        media_uploader = MediaUploader(provider_registry=registry)

        # Act & Assert
        with pytest.raises(CannotUploadMediaProviderDoesNotSupportUploadException):
            await media_uploader.upload(provider_name="noupload", media=test_media)

    @pytest.mark.asyncio
    async def test_upload_with_valid_provider_name_should_return_upload_result(
        self, single_provider_media_uploader: MediaUploader, mock_provider, test_media: ExternalMedia
    ):
        """Should successfully upload media and return the result from provider."""
        # Arrange: Set up mock return value
        mock_provider.upload.return_value = True

        # Act
        result = await single_provider_media_uploader.upload(provider_name="mockprovider", media=test_media)

        # Assert
        assert result is True
        mock_provider.upload.assert_called_once_with(test_media)

    @pytest.mark.asyncio
    async def test_upload_with_valid_provider_name_but_upload_fails_should_return_false(
        self, single_provider_media_uploader: MediaUploader, mock_provider, test_media: ExternalMedia
    ):
        """Should return False when provider upload fails."""
        # Arrange
        mock_provider.upload.return_value = False

        # Act
        result = await single_provider_media_uploader.upload(provider_name="mockprovider", media=test_media)

        # Assert
        assert result is False
        mock_provider.upload.assert_called_once_with(test_media)

    @pytest.mark.asyncio
    async def test_upload_with_multiple_providers_should_upload_to_correct_provider(
        self, multiple_providers_media_uploader: MediaUploader, test_media: ExternalMedia
    ):
        """Should upload media to the correct provider when multiple providers are registered."""
        # Arrange
        providers = multiple_providers_media_uploader.provider_registry.get_providers()
        provider2 = providers[1]  # mockprovider2
        provider2.upload.return_value = True

        # Act
        result = await multiple_providers_media_uploader.upload(provider_name="mockprovider2", media=test_media)

        # Assert
        assert result is True
        provider2.upload.assert_called_once_with(test_media)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "invalid_provider_name",
        ["nonexistentprovider", None, ""],
        ids=["nonexistent", "none", "empty"],
    )
    async def test_upload_with_multiple_providers_and_invalid_name_should_raise_error(
        self, multiple_providers_media_uploader: MediaUploader, test_media: ExternalMedia, invalid_provider_name
    ):
        """Should raise exception even with multiple providers when provider name is invalid."""
        with pytest.raises(CannotUploadMediaWithInvalidProviderNameException):
            await multiple_providers_media_uploader.upload(provider_name=invalid_provider_name, media=test_media)

    @pytest.mark.asyncio
    async def test_upload_with_no_providers_should_raise_error(
        self, empty_provider_media_uploader: MediaUploader, test_media: ExternalMedia
    ):
        """Should raise exception when no providers are registered."""
        with pytest.raises(CannotUploadMediaWithoutRegisteredProvidersException):
            await empty_provider_media_uploader.upload(provider_name="anyprovider", media=test_media)


class TestMediaUploaderUploadToMultiple:
    """Test suite for MediaUploader.upload_to_multiple() method."""

    @pytest.mark.asyncio
    async def test_upload_to_multiple_with_valid_providers_should_return_results_dict(
        self, multiple_providers_media_uploader: MediaUploader, test_media: ExternalMedia
    ):
        """Should upload to multiple providers and return results dictionary."""
        # Arrange
        providers = multiple_providers_media_uploader.provider_registry.get_providers()
        provider1, provider2 = providers[0], providers[1]
        provider1.upload.return_value = True
        provider2.upload.return_value = False

        # Act
        results = await multiple_providers_media_uploader.upload_to_multiple(
            media=test_media, providers=["mockprovider", "mockprovider2"]
        )

        # Assert
        assert isinstance(results, dict)
        assert len(results) == 2
        assert results["mockprovider"] is True
        assert results["mockprovider2"] is False
        provider1.upload.assert_called_once_with(test_media)
        provider2.upload.assert_called_once_with(test_media)

    @pytest.mark.asyncio
    async def test_upload_to_multiple_with_empty_provider_list_should_return_empty_dict(
        self, single_provider_media_uploader: MediaUploader, test_media: ExternalMedia
    ):
        """Should return empty dict when no providers specified."""
        # Act
        results = await single_provider_media_uploader.upload_to_multiple(media=test_media, providers=[])

        # Assert
        assert isinstance(results, dict)
        assert len(results) == 0

    @pytest.mark.asyncio
    async def test_upload_to_multiple_with_invalid_provider_name_should_raise_error(
        self, single_provider_media_uploader: MediaUploader, test_media: ExternalMedia
    ):
        """Should raise exception when one of the providers is invalid."""
        with pytest.raises(CannotUploadMediaToMultipleWithInvalidProviderNameException):
            await single_provider_media_uploader.upload_to_multiple(
                media=test_media, providers=["mockprovider", "nonexistent"]
            )

    @pytest.mark.asyncio
    async def test_upload_to_multiple_with_provider_that_does_not_support_upload_should_raise_error(
        self, test_media: ExternalMedia
    ):
        """Should raise exception when one of the providers does not support upload."""
        # Arrange
        upload_provider = create_mock_provider("upload")
        no_upload_provider = create_mock_provider_without_upload("noupload")
        registry = create_mock_registry([upload_provider, no_upload_provider])
        media_uploader = MediaUploader(provider_registry=registry)

        # Act & Assert
        with pytest.raises(CannotUploadMediaProviderDoesNotSupportUploadException):
            await media_uploader.upload_to_multiple(media=test_media, providers=["upload", "noupload"])

    @pytest.mark.asyncio
    async def test_upload_to_multiple_with_no_providers_registered_should_raise_error(
        self, empty_provider_media_uploader: MediaUploader, test_media: ExternalMedia
    ):
        """Should raise exception when no providers are registered."""
        with pytest.raises(CannotUploadMediaToMultipleWithoutRegisteredProvidersException):
            await empty_provider_media_uploader.upload_to_multiple(media=test_media, providers=["anyprovider"])

    @pytest.mark.asyncio
    async def test_upload_to_multiple_with_mixed_results_should_return_correct_results(self, test_media: ExternalMedia):
        """Should handle mixed success/failure results correctly."""
        # Arrange
        provider1 = create_mock_provider("success")
        provider2 = create_mock_provider("failure")
        provider3 = create_mock_provider("another_success")

        provider1.upload.return_value = True
        provider2.upload.return_value = False
        provider3.upload.return_value = True

        registry = create_mock_registry([provider1, provider2, provider3])
        media_uploader = MediaUploader(provider_registry=registry)

        # Act
        results = await media_uploader.upload_to_multiple(
            media=test_media, providers=["success", "failure", "another_success"]
        )

        # Assert
        assert results == {"success": True, "failure": False, "another_success": True}
        provider1.upload.assert_called_once_with(test_media)
        provider2.upload.assert_called_once_with(test_media)
        provider3.upload.assert_called_once_with(test_media)
