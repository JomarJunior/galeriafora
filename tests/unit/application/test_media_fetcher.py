"""
Unit tests for MediaFetcher application service.

This test suite validates the MediaFetcher's orchestration logic, ensuring proper
coordination with the ProviderRegistry and IExternalProvider interface according to
hexagonal architecture principles.

Tests use unittest.mock for creating test doubles and verifying interactions.
"""

from typing import Optional, Sequence
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
    MediaFetcher,
    Page,
    ProviderRegistry,
)
from galeriafora.domain.exceptions import (
    CannotFetchLatestMediaProviderDoesNotSupportFetchLatestException,
    CannotFetchLatestMediaWithInvalidProviderNameException,
    CannotFetchLatestMediaWithoutRegisteredProvidersException,
    CannotFetchMediaByTagsProviderDoesNotSupportFetchByTagsException,
    CannotFetchMediaByTagsWithInvalidProviderNameException,
    CannotFetchMediaByTagsWithoutRegisteredProvidersException,
    CannotFetchMediaByUserProviderDoesNotSupportFetchByUserException,
    CannotFetchMediaByUserWithInvalidProviderNameException,
    CannotFetchMediaByUserWithoutRegisteredProvidersException,
    CannotInitializeMediaFetcherWithInvalidProviderRegistryException,
)

# Constants following architecture documentation (default limit is 200)
DEFAULT_LIMIT = 200
TEST_LIMIT = 10


# Helper functions for creating test data
def create_test_media(
    index: int,
    url_pattern: str,
    title_pattern: str,
    tags_pattern: callable,
    provider_name: str = "mockprovider",
) -> ExternalMedia:
    """Helper function to create test media items with consistent structure."""
    return ExternalMedia(
        url=url_pattern.format(index),
        title=title_pattern.format(index),
        description=f"Description for {title_pattern.format(index).lower()}",
        content_metadata=ContentMetadata(
            content_type=ContentType.IMAGE_JPEG,
            dimensions={"width": 800, "height": 600},
            file_size_bytes=150000,
        ),
        tags=tags_pattern(index),
        mature_rating=MatureRating.PG,
        ai_metadata=AiMetadata(is_ai_generated=False),
        provider=ExternalProviderInfo(
            name=ExternalProviderName(provider_name),
            description="A mock provider for testing.",
            capabilities=[
                ExternalProviderCapability.FETCH_LATEST,
                ExternalProviderCapability.FETCH_BY_USER,
                ExternalProviderCapability.FETCH_BY_TAGS,
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
        ],
    )

    # Mock async methods with AsyncMock
    mock_provider.fetch_latest = AsyncMock()
    mock_provider.fetch_by_user = AsyncMock()
    mock_provider.fetch_by_tags = AsyncMock()

    return mock_provider


def create_mock_provider_without_fetch_latest(name: str = "nofetchlatest") -> Mock:
    """Create a mock IExternalProvider without FETCH_LATEST capability."""
    mock_provider = Mock(spec=IExternalProvider)

    # Set up provider info property without FETCH_LATEST
    mock_provider.info = ExternalProviderInfo(
        name=ExternalProviderName(name),
        description="A mock provider without fetch latest capability.",
        capabilities=[
            ExternalProviderCapability.FETCH_BY_USER,
            ExternalProviderCapability.FETCH_BY_TAGS,
        ],
    )

    # Mock async methods with AsyncMock (except fetch_latest which shouldn't be called)
    mock_provider.fetch_by_user = AsyncMock()
    mock_provider.fetch_by_tags = AsyncMock()

    return mock_provider


def create_mock_provider_without_fetch_by_user(name: str = "nofetchbyuser") -> Mock:
    """Create a mock IExternalProvider without FETCH_BY_USER capability."""
    mock_provider = Mock(spec=IExternalProvider)

    # Set up provider info property without FETCH_BY_USER
    mock_provider.info = ExternalProviderInfo(
        name=ExternalProviderName(name),
        description="A mock provider without fetch by user capability.",
        capabilities=[
            ExternalProviderCapability.FETCH_LATEST,
            ExternalProviderCapability.FETCH_BY_TAGS,
        ],
    )

    # Mock async methods with AsyncMock (except fetch_by_user which shouldn't be called)
    mock_provider.fetch_latest = AsyncMock()
    mock_provider.fetch_by_tags = AsyncMock()

    return mock_provider


def create_mock_provider_without_fetch_by_tags(name: str = "nofetchbytags") -> Mock:
    """Create a mock IExternalProvider without FETCH_BY_TAGS capability."""
    mock_provider = Mock(spec=IExternalProvider)

    # Set up provider info property without FETCH_BY_TAGS
    mock_provider.info = ExternalProviderInfo(
        name=ExternalProviderName(name),
        description="A mock provider without fetch by tags capability.",
        capabilities=[
            ExternalProviderCapability.FETCH_LATEST,
            ExternalProviderCapability.FETCH_BY_USER,
        ],
    )

    # Mock async methods with AsyncMock (except fetch_by_tags which shouldn't be called)
    mock_provider.fetch_latest = AsyncMock()
    mock_provider.fetch_by_user = AsyncMock()

    return mock_provider


def create_mock_registry(providers: list) -> Mock:
    """Create a mock ProviderRegistry using unittest.mock."""
    mock_registry = Mock(spec=ProviderRegistry)
    mock_registry.get_providers.return_value = providers
    return mock_registry


@pytest.fixture
def mock_provider() -> Mock:
    """Fixture providing a single mock provider."""
    return create_mock_provider()


@pytest.fixture
def mock_provider_registry(mock_provider) -> Mock:
    """Fixture providing a mock registry with a single provider."""
    return create_mock_registry([mock_provider])


@pytest.fixture
def single_provider_media_fetcher(mock_provider_registry) -> MediaFetcher:
    """Fixture providing a MediaFetcher with a single mock provider."""
    return MediaFetcher(provider_registry=mock_provider_registry)


@pytest.fixture
def multiple_providers_media_fetcher() -> MediaFetcher:
    """Fixture providing a MediaFetcher with multiple mock providers."""
    provider1 = create_mock_provider("mockprovider")
    provider2 = create_mock_provider("mockprovider2")
    registry = create_mock_registry([provider1, provider2])
    return MediaFetcher(provider_registry=registry)


@pytest.fixture
def empty_provider_media_fetcher() -> MediaFetcher:
    """Fixture providing a MediaFetcher with no registered providers."""
    registry = create_mock_registry([])
    return MediaFetcher(provider_registry=registry)


class TestMediaFetcherInitialization:
    """Test suite for MediaFetcher initialization."""

    def test_initialization_with_single_provider(self, single_provider_media_fetcher: MediaFetcher, mock_provider):
        """Should successfully initialize MediaFetcher with a single provider."""
        assert isinstance(single_provider_media_fetcher, MediaFetcher)
        providers = single_provider_media_fetcher.provider_registry.get_providers()
        assert len(providers) == 1
        assert providers[0].info.name == "mockprovider"

    def test_initialization_with_multiple_providers(self, multiple_providers_media_fetcher: MediaFetcher):
        """Should successfully initialize MediaFetcher with multiple providers."""
        assert isinstance(multiple_providers_media_fetcher, MediaFetcher)
        providers = multiple_providers_media_fetcher.provider_registry.get_providers()
        assert len(providers) == 2
        provider_names = [provider.info.name for provider in providers]
        assert "mockprovider" in provider_names
        assert "mockprovider2" in provider_names

    def test_initialization_with_no_providers(self, empty_provider_media_fetcher: MediaFetcher):
        """Should successfully initialize MediaFetcher even with no providers."""
        assert isinstance(empty_provider_media_fetcher, MediaFetcher)
        assert len(empty_provider_media_fetcher.provider_registry.get_providers()) == 0

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
        with pytest.raises(CannotInitializeMediaFetcherWithInvalidProviderRegistryException):
            MediaFetcher(provider_registry=invalid_registry)

    def test_initialization_with_none_provider_registry_should_raise_error(self):
        """Should raise exception when initializing with None as provider registry."""
        with pytest.raises(CannotInitializeMediaFetcherWithInvalidProviderRegistryException):
            MediaFetcher(provider_registry=None)


class TestMediaFetcherFetchLatest:
    """Test suite for MediaFetcher.fetch_latest() method."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "invalid_provider_name",
        ["nonexistentprovider", None, ""],
        ids=["nonexistent", "none", "empty"],
    )
    async def test_fetch_latest_with_invalid_provider_name_should_raise_error(
        self, single_provider_media_fetcher: MediaFetcher, invalid_provider_name
    ):
        """Should raise exception when fetching with invalid provider names."""
        with pytest.raises(CannotFetchLatestMediaWithInvalidProviderNameException):
            await single_provider_media_fetcher.fetch_latest(provider_name=invalid_provider_name)

    @pytest.mark.asyncio
    async def test_fetch_latest_with_valid_provider_name_should_return_media_from_provider(
        self, single_provider_media_fetcher: MediaFetcher, mock_provider
    ):
        """Should successfully fetch media from valid provider with correct structure."""
        # Arrange: Set up mock return value
        expected_media = [
            create_test_media(i, "https://example.com/media{}.jpg", "Media {}", lambda idx: [f"tag{idx}", "latest"])
            for i in range(1, TEST_LIMIT + 1)
        ]
        mock_provider.fetch_latest.return_value = Page(
            items=expected_media,
            next_cursor=None,
            has_more=False,
        )

        # Act
        media_page = await single_provider_media_fetcher.fetch_latest(provider_name="mockprovider", limit=TEST_LIMIT)

        # Assert
        assert isinstance(media_page, Page)
        assert len(media_page.items) == TEST_LIMIT
        assert media_page.next_cursor is None
        assert media_page.has_more is False

        # Verify mock was called correctly
        mock_provider.fetch_latest.assert_called_once_with(limit=TEST_LIMIT)

        for index, media in enumerate(media_page.items, start=1):
            assert media.url == f"https://example.com/media{index}.jpg"
            assert media.title == f"Media {index}"

    @pytest.mark.asyncio
    async def test_fetch_latest_with_default_limit_should_use_architecture_default(
        self, single_provider_media_fetcher: MediaFetcher, mock_provider
    ):
        """Should use default limit of 200 items as per architecture specification."""
        # Arrange
        expected_media = [
            create_test_media(i, "https://example.com/media{}.jpg", "Media {}", lambda idx: [f"tag{idx}", "latest"])
            for i in range(1, DEFAULT_LIMIT + 1)
        ]
        mock_provider.fetch_latest.return_value = Page(items=expected_media, next_cursor=None, has_more=False)

        # Act
        media_page = await single_provider_media_fetcher.fetch_latest(provider_name="mockprovider")

        # Assert
        assert isinstance(media_page, Page)
        assert len(media_page.items) == DEFAULT_LIMIT
        mock_provider.fetch_latest.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_latest_with_valid_provider_name_but_no_media_should_return_empty_page(self):
        """Should return empty page when provider has no media available."""
        # Arrange
        empty_provider = create_mock_provider("emptymedia")
        empty_provider.fetch_latest.return_value = Page(items=[], next_cursor=None, has_more=False)
        registry = create_mock_registry([empty_provider])
        media_fetcher = MediaFetcher(provider_registry=registry)

        # Act
        media_page = await media_fetcher.fetch_latest(provider_name="emptymedia", limit=TEST_LIMIT)

        # Assert
        assert isinstance(media_page, Page)
        assert len(media_page.items) == 0
        assert media_page.next_cursor is None
        assert media_page.has_more is False
        empty_provider.fetch_latest.assert_called_once_with(limit=TEST_LIMIT)

    @pytest.mark.asyncio
    async def test_fetch_latest_with_multiple_providers_should_return_media_from_correct_provider(
        self, multiple_providers_media_fetcher: MediaFetcher
    ):
        """Should fetch media from the correct provider when multiple providers are registered."""
        # Arrange
        providers = multiple_providers_media_fetcher.provider_registry.get_providers()
        provider2 = providers[1]  # mockprovider2
        expected_media = [
            create_test_media(
                i, "https://example.com/media{}.jpg", "Media {}", lambda idx: [f"tag{idx}", "latest"], "mockprovider2"
            )
            for i in range(1, 6)
        ]
        provider2.fetch_latest.return_value = Page(items=expected_media, next_cursor=None, has_more=False)

        # Act
        media_page = await multiple_providers_media_fetcher.fetch_latest(provider_name="mockprovider2", limit=5)

        # Assert
        assert isinstance(media_page, Page)
        assert len(media_page.items) == 5
        provider2.fetch_latest.assert_called_once_with(limit=5)

        # Verify all items are from the correct provider
        for media in media_page.items:
            assert media.provider.name == "mockprovider2"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "invalid_provider_name",
        ["nonexistentprovider", None, ""],
        ids=["nonexistent", "none", "empty"],
    )
    async def test_fetch_latest_with_multiple_providers_and_invalid_name_should_raise_error(
        self, multiple_providers_media_fetcher: MediaFetcher, invalid_provider_name
    ):
        """Should raise exception even with multiple providers when provider name is invalid."""
        with pytest.raises(CannotFetchLatestMediaWithInvalidProviderNameException):
            await multiple_providers_media_fetcher.fetch_latest(provider_name=invalid_provider_name)

    @pytest.mark.asyncio
    async def test_fetch_latest_with_no_providers_should_raise_error(self, empty_provider_media_fetcher: MediaFetcher):
        """Should raise exception when no providers are registered."""
        with pytest.raises(CannotFetchLatestMediaWithoutRegisteredProvidersException):
            await empty_provider_media_fetcher.fetch_latest(provider_name="anyprovider")

    @pytest.mark.asyncio
    async def test_fetch_latest_with_provider_that_does_not_support_fetch_latest_should_raise_error(self):
        """Should raise exception when provider does not support FETCH_LATEST capability."""
        # Arrange
        no_fetch_latest_provider = create_mock_provider_without_fetch_latest("nofetchlatest")
        registry = create_mock_registry([no_fetch_latest_provider])
        media_fetcher = MediaFetcher(provider_registry=registry)

        # Act & Assert
        with pytest.raises(CannotFetchLatestMediaProviderDoesNotSupportFetchLatestException):
            await media_fetcher.fetch_latest(provider_name="nofetchlatest")


class TestMediaFetcherFetchByUser:
    """Test suite for MediaFetcher.fetch_by_user() method."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "invalid_provider_name",
        ["nonexistentprovider", None, ""],
        ids=["nonexistent", "none", "empty"],
    )
    async def test_fetch_by_user_with_invalid_provider_name_should_raise_error(
        self, single_provider_media_fetcher: MediaFetcher, invalid_provider_name
    ):
        """Should raise exception when fetching by user with invalid provider names."""
        with pytest.raises(CannotFetchMediaByUserWithInvalidProviderNameException):
            await single_provider_media_fetcher.fetch_by_user(provider_name=invalid_provider_name, username="user1")

    @pytest.mark.asyncio
    async def test_fetch_by_user_with_valid_provider_name_but_nonexistent_user_should_return_empty_page(
        self, single_provider_media_fetcher: MediaFetcher, mock_provider
    ):
        """Should return empty page when user does not exist."""
        # Arrange
        mock_provider.fetch_by_user.return_value = Page(items=[], next_cursor=None, has_more=False)

        # Act
        media_page = await single_provider_media_fetcher.fetch_by_user(
            provider_name="mockprovider", username="nonexistentuser"
        )

        # Assert
        assert isinstance(media_page, Page)
        assert len(media_page.items) == 0
        assert media_page.next_cursor is None
        assert media_page.has_more is False
        mock_provider.fetch_by_user.assert_called_once_with("nonexistentuser", limit=DEFAULT_LIMIT)

    @pytest.mark.asyncio
    async def test_fetch_by_user_with_valid_provider_name_and_existing_user_should_return_media(
        self, single_provider_media_fetcher: MediaFetcher, mock_provider
    ):
        """Should successfully fetch media for existing user."""
        # Arrange
        expected_media = [
            create_test_media(
                i,
                "https://example.com/user1_media{}.jpg",
                "User User1 Media {}",
                lambda idx: [f"user1_tag{idx}", "user"],
            )
            for i in range(1, 6)
        ]
        mock_provider.fetch_by_user.return_value = Page(items=expected_media, next_cursor=None, has_more=False)

        # Act
        media_page = await single_provider_media_fetcher.fetch_by_user(
            provider_name="mockprovider", username="user1", limit=5
        )

        # Assert
        assert isinstance(media_page, Page)
        assert len(media_page.items) == 5
        mock_provider.fetch_by_user.assert_called_once_with("user1", limit=5)

        for index, media in enumerate(media_page.items, start=1):
            assert media.url == f"https://example.com/user1_media{index}.jpg"
            assert f"user1_tag{index}" in media.tags
            assert "user" in media.tags
            assert media.provider.name == "mockprovider"

    @pytest.mark.asyncio
    async def test_fetch_by_user_with_valid_provider_name_and_existing_user_but_no_media_should_return_empty_page(
        self, single_provider_media_fetcher: MediaFetcher, mock_provider
    ):
        """Should return empty page when user exists but has no media."""
        # Arrange
        mock_provider.fetch_by_user.return_value = Page(items=[], next_cursor=None, has_more=False)

        # Act
        media_page = await single_provider_media_fetcher.fetch_by_user(provider_name="mockprovider", username="user2")

        # Assert
        assert isinstance(media_page, Page)
        assert len(media_page.items) == 0
        assert media_page.next_cursor is None
        assert media_page.has_more is False
        mock_provider.fetch_by_user.assert_called_once_with("user2", limit=DEFAULT_LIMIT)

    @pytest.mark.asyncio
    async def test_fetch_by_user_with_multiple_providers_should_return_media_from_correct_provider(
        self, multiple_providers_media_fetcher: MediaFetcher
    ):
        """Should fetch media from the correct provider when multiple providers are registered."""
        # Arrange
        providers = multiple_providers_media_fetcher.provider_registry.get_providers()
        provider2 = providers[1]
        expected_media = [
            create_test_media(
                i,
                "https://example.com/user1_media{}.jpg",
                "User User1 Media {}",
                lambda idx: [f"user1_tag{idx}", "user"],
                "mockprovider2",
            )
            for i in range(1, 6)
        ]
        provider2.fetch_by_user.return_value = Page(items=expected_media, next_cursor=None, has_more=False)

        # Act
        media_page = await multiple_providers_media_fetcher.fetch_by_user(
            provider_name="mockprovider2", username="user1", limit=5
        )

        # Assert
        assert isinstance(media_page, Page)
        assert len(media_page.items) == 5
        provider2.fetch_by_user.assert_called_once_with("user1", limit=5)

        # Verify all items are from the correct provider
        for media in media_page.items:
            assert media.provider.name == "mockprovider2"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "invalid_provider_name",
        ["nonexistentprovider", None, ""],
        ids=["nonexistent", "none", "empty"],
    )
    async def test_fetch_by_user_with_multiple_providers_and_invalid_name_should_raise_error(
        self, multiple_providers_media_fetcher: MediaFetcher, invalid_provider_name
    ):
        """Should raise exception even with multiple providers when provider name is invalid."""
        with pytest.raises(CannotFetchMediaByUserWithInvalidProviderNameException):
            await multiple_providers_media_fetcher.fetch_by_user(provider_name=invalid_provider_name, username="user1")

    @pytest.mark.asyncio
    async def test_fetch_by_user_with_no_providers_should_raise_error(self, empty_provider_media_fetcher: MediaFetcher):
        """Should raise exception when no providers are registered."""
        with pytest.raises(CannotFetchMediaByUserWithoutRegisteredProvidersException):
            await empty_provider_media_fetcher.fetch_by_user(provider_name="anyprovider", username="user1")

    @pytest.mark.asyncio
    async def test_fetch_by_user_with_provider_that_does_not_support_fetch_by_user_should_raise_error(self):
        """Should raise exception when provider does not support FETCH_BY_USER capability."""
        # Arrange
        no_fetch_by_user_provider = create_mock_provider_without_fetch_by_user("nofetchbyuser")
        registry = create_mock_registry([no_fetch_by_user_provider])
        media_fetcher = MediaFetcher(provider_registry=registry)

        # Act & Assert
        with pytest.raises(CannotFetchMediaByUserProviderDoesNotSupportFetchByUserException):
            await media_fetcher.fetch_by_user(provider_name="nofetchbyuser", username="user1")


class TestMediaFetcherFetchByTags:
    """Test suite for MediaFetcher.fetch_by_tags() method."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "invalid_provider_name",
        ["nonexistentprovider", None, ""],
        ids=["nonexistent", "none", "empty"],
    )
    async def test_fetch_by_tags_with_invalid_provider_name_should_raise_error(
        self, single_provider_media_fetcher: MediaFetcher, invalid_provider_name
    ):
        """Should raise exception when fetching by tags with invalid provider names."""
        with pytest.raises(CannotFetchMediaByTagsWithInvalidProviderNameException):
            await single_provider_media_fetcher.fetch_by_tags(
                provider_name=invalid_provider_name, tags=["latest", "tag1"]
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "tags,expected_count",
        [
            (["nonexistenttag"], 0),
            (["tag2", "latest"], 0),
            ([], 0),
            (None, 0),
            (["latest", "nonexistenttag"], 0),
        ],
        ids=["nonexistent_tags", "empty_result_tags", "empty_list", "none", "partial_match"],
    )
    async def test_fetch_by_tags_with_various_tag_scenarios_should_return_empty_page(
        self, single_provider_media_fetcher: MediaFetcher, mock_provider, tags, expected_count
    ):
        """Should return empty page for various non-matching tag scenarios."""
        # Arrange
        mock_provider.fetch_by_tags.return_value = Page(items=[], next_cursor=None, has_more=False)

        # Act
        media_page = await single_provider_media_fetcher.fetch_by_tags(provider_name="mockprovider", tags=tags)

        # Assert
        assert isinstance(media_page, Page)
        assert len(media_page.items) == expected_count
        assert media_page.next_cursor is None
        assert media_page.has_more is False
        mock_provider.fetch_by_tags.assert_called_once_with(tags, limit=DEFAULT_LIMIT)

    @pytest.mark.asyncio
    async def test_fetch_by_tags_with_valid_provider_name_and_existing_tags_should_return_media(
        self, single_provider_media_fetcher: MediaFetcher, mock_provider
    ):
        """Should successfully fetch media when tags match."""
        # Arrange
        expected_media = [
            create_test_media(
                i, "https://example.com/tag1_media{}.jpg", "Tag1 Media {}", lambda idx: [f"tag1_tag{idx}", "tag"]
            )
            for i in range(1, 6)
        ]
        mock_provider.fetch_by_tags.return_value = Page(items=expected_media, next_cursor=None, has_more=False)

        # Act
        media_page = await single_provider_media_fetcher.fetch_by_tags(
            provider_name="mockprovider", tags=["tag1", "latest"], limit=5
        )

        # Assert
        assert isinstance(media_page, Page)
        assert len(media_page.items) == 5
        mock_provider.fetch_by_tags.assert_called_once_with(["tag1", "latest"], limit=5)

        for index, media in enumerate(media_page.items, start=1):
            assert media.url == f"https://example.com/tag1_media{index}.jpg"
            assert media.title == f"Tag1 Media {index}"
            assert f"tag1_tag{index}" in media.tags
            assert "tag" in media.tags
            assert media.provider.name == "mockprovider"

    @pytest.mark.asyncio
    async def test_fetch_by_tags_with_multiple_providers_should_return_media_from_correct_provider(
        self, multiple_providers_media_fetcher: MediaFetcher
    ):
        """Should fetch media from the correct provider when multiple providers are registered."""
        # Arrange
        providers = multiple_providers_media_fetcher.provider_registry.get_providers()
        provider2 = providers[1]
        expected_media = [
            create_test_media(
                i,
                "https://example.com/tag1_media{}.jpg",
                "Tag1 Media {}",
                lambda idx: [f"tag1_tag{idx}", "tag"],
                "mockprovider2",
            )
            for i in range(1, 6)
        ]
        provider2.fetch_by_tags.return_value = Page(items=expected_media, next_cursor=None, has_more=False)

        # Act
        media_page = await multiple_providers_media_fetcher.fetch_by_tags(
            provider_name="mockprovider2", tags=["tag1", "latest"], limit=5
        )

        # Assert
        assert isinstance(media_page, Page)
        assert len(media_page.items) == 5
        provider2.fetch_by_tags.assert_called_once_with(["tag1", "latest"], limit=5)

        # Verify all items are from the correct provider
        for media in media_page.items:
            assert media.provider.name == "mockprovider2"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "invalid_provider_name",
        ["nonexistentprovider", None, ""],
        ids=["nonexistent", "none", "empty"],
    )
    async def test_fetch_by_tags_with_multiple_providers_and_invalid_name_should_raise_error(
        self, multiple_providers_media_fetcher: MediaFetcher, invalid_provider_name
    ):
        """Should raise exception even with multiple providers when provider name is invalid."""
        with pytest.raises(CannotFetchMediaByTagsWithInvalidProviderNameException):
            await multiple_providers_media_fetcher.fetch_by_tags(
                provider_name=invalid_provider_name, tags=["latest", "tag1"]
            )

    @pytest.mark.asyncio
    async def test_fetch_by_tags_with_no_providers_should_raise_error(self, empty_provider_media_fetcher: MediaFetcher):
        """Should raise exception when no providers are registered."""
        with pytest.raises(CannotFetchMediaByTagsWithoutRegisteredProvidersException):
            await empty_provider_media_fetcher.fetch_by_tags(provider_name="anyprovider", tags=["latest", "tag1"])

    @pytest.mark.asyncio
    async def test_fetch_by_tags_with_provider_that_does_not_support_fetch_by_tags_should_raise_error(self):
        """Should raise exception when provider does not support FETCH_BY_TAGS capability."""
        # Arrange
        no_fetch_by_tags_provider = create_mock_provider_without_fetch_by_tags("nofetchbytags")
        registry = create_mock_registry([no_fetch_by_tags_provider])
        media_fetcher = MediaFetcher(provider_registry=registry)

        # Act & Assert
        with pytest.raises(CannotFetchMediaByTagsProviderDoesNotSupportFetchByTagsException):
            await media_fetcher.fetch_by_tags(provider_name="nofetchbytags", tags=["latest", "tag1"])
