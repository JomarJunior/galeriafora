"""
Unit tests for ProviderCoordinator application service.

This test suite validates the ProviderCoordinator's provider management logic, ensuring proper
discovery and coordination with the ProviderRegistry according to hexagonal architecture principles.

Tests use unittest.mock for creating test doubles and verifying interactions.
"""

from unittest.mock import Mock

import pytest

from galeriafora import (
    ExternalProviderCapability,
    ExternalProviderInfo,
    ExternalProviderName,
    IExternalProvider,
    ProviderCoordinator,
    ProviderRegistry,
)
from galeriafora.domain.exceptions import (
    CannotGetProviderWithInvalidNameException,
    CannotInitializeProviderCoordinatorWithInvalidProviderRegistryException,
)


# Helper functions for creating test data
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

    return mock_provider


def create_mock_provider_fetch_only(name: str = "fetchonlyprovider") -> Mock:
    """Create a mock IExternalProvider with only fetch capabilities."""
    mock_provider = Mock(spec=IExternalProvider)

    # Set up provider info property with only fetch capabilities
    mock_provider.info = ExternalProviderInfo(
        name=ExternalProviderName(name),
        description="A mock provider with only fetch capabilities.",
        capabilities=[
            ExternalProviderCapability.FETCH_LATEST,
            ExternalProviderCapability.FETCH_BY_USER,
            ExternalProviderCapability.FETCH_BY_TAGS,
        ],
    )

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
def mock_provider_without_upload() -> Mock:
    """Fixture providing a mock provider without upload capability."""
    return create_mock_provider_without_upload()


@pytest.fixture
def mock_provider_fetch_only() -> Mock:
    """Fixture providing a mock provider with only fetch capabilities."""
    return create_mock_provider_fetch_only()


@pytest.fixture
def mock_provider_registry_single(mock_provider) -> Mock:
    """Fixture providing a mock registry with a single provider."""
    return create_mock_registry([mock_provider])


@pytest.fixture
def mock_provider_registry_multiple() -> Mock:
    """Fixture providing a mock registry with multiple providers."""
    provider1 = create_mock_provider("mockprovider1")
    provider2 = create_mock_provider("mockprovider2")
    provider3 = create_mock_provider_without_upload("nouploadprovider")
    return create_mock_registry([provider1, provider2, provider3])


@pytest.fixture
def mock_provider_registry_empty() -> Mock:
    """Fixture providing a mock registry with no providers."""
    return create_mock_registry([])


@pytest.fixture
def single_provider_coordinator(mock_provider_registry_single) -> ProviderCoordinator:
    """Fixture providing a ProviderCoordinator with a single provider."""
    return ProviderCoordinator(provider_registry=mock_provider_registry_single)


@pytest.fixture
def multiple_providers_coordinator(mock_provider_registry_multiple) -> ProviderCoordinator:
    """Fixture providing a ProviderCoordinator with multiple providers."""
    return ProviderCoordinator(provider_registry=mock_provider_registry_multiple)


@pytest.fixture
def empty_provider_coordinator(mock_provider_registry_empty) -> ProviderCoordinator:
    """Fixture providing a ProviderCoordinator with no providers."""
    return ProviderCoordinator(provider_registry=mock_provider_registry_empty)


# class TestProviderCoordinatorInitialization:
#     """Test suite for ProviderCoordinator initialization."""

#     def test_initialization_with_single_provider(self, single_provider_coordinator: ProviderCoordinator):
#         """Should successfully initialize ProviderCoordinator with a single provider."""
#         assert isinstance(single_provider_coordinator, ProviderCoordinator)
#         providers = single_provider_coordinator.provider_registry.get_providers()
#         assert len(providers) == 1
#         assert providers[0].info.name == "mockprovider"

#     def test_initialization_with_multiple_providers(self, multiple_providers_coordinator: ProviderCoordinator):
#         """Should successfully initialize ProviderCoordinator with multiple providers."""
#         assert isinstance(multiple_providers_coordinator, ProviderCoordinator)
#         providers = multiple_providers_coordinator.provider_registry.get_providers()
#         assert len(providers) == 3
#         provider_names = [provider.info.name for provider in providers]
#         assert "mockprovider1" in provider_names
#         assert "mockprovider2" in provider_names
#         assert "nouploadprovider" in provider_names

#     def test_initialization_with_no_providers(self, empty_provider_coordinator: ProviderCoordinator):
#         """Should successfully initialize ProviderCoordinator even with no providers."""
#         assert isinstance(empty_provider_coordinator, ProviderCoordinator)
#         assert len(empty_provider_coordinator.provider_registry.get_providers()) == 0

#     @pytest.mark.parametrize(
#         "invalid_registry",
#         [
#             "not a registry",
#             123,
#             [],
#             {},
#         ],
#         ids=["string", "integer", "list", "dict"],
#     )
#     def test_initialization_with_invalid_provider_registry_should_raise_error(self, invalid_registry):
#         """Should raise exception when initializing with invalid provider registry types."""
#         with pytest.raises(CannotInitializeProviderCoordinatorWithInvalidProviderRegistryException):
#             ProviderCoordinator(provider_registry=invalid_registry)

#     def test_initialization_with_none_provider_registry_should_raise_error(self):
#         """Should raise exception when initializing with None as provider registry."""
#         with pytest.raises(CannotInitializeProviderCoordinatorWithInvalidProviderRegistryException):
#             ProviderCoordinator(provider_registry=None)


class TestProviderCoordinatorGetProvider:
    """Test suite for ProviderCoordinator.get_provider() method."""

    def test_get_provider_with_valid_name_should_return_provider(
        self, single_provider_coordinator: ProviderCoordinator, mock_provider
    ):
        """Should successfully return provider when valid name is provided."""
        provider = single_provider_coordinator.get_provider(ExternalProviderName("mockprovider"))
        assert provider is mock_provider
        assert provider.info.name == "mockprovider"

    def test_get_provider_with_valid_name_from_multiple_providers_should_return_correct_provider(
        self, multiple_providers_coordinator: ProviderCoordinator
    ):
        """Should return the correct provider when multiple providers are available."""
        provider = multiple_providers_coordinator.get_provider(ExternalProviderName("mockprovider2"))
        assert provider.info.name == "mockprovider2"

    @pytest.mark.parametrize(
        "invalid_name",
        ["nonexistentprovider", None, ""],
        ids=["nonexistent", "none", "empty"],
    )
    def test_get_provider_with_invalid_name_should_raise_error(
        self, single_provider_coordinator: ProviderCoordinator, invalid_name
    ):
        """Should raise exception when provider name is invalid or not found."""
        with pytest.raises(CannotGetProviderWithInvalidNameException):
            single_provider_coordinator.get_provider(ExternalProviderName(invalid_name))

    def test_get_provider_with_no_providers_should_raise_error(self, empty_provider_coordinator: ProviderCoordinator):
        """Should raise exception when no providers are registered."""
        with pytest.raises(CannotGetProviderWithInvalidNameException):
            empty_provider_coordinator.get_provider(ExternalProviderName("anyprovider"))


class TestProviderCoordinatorListProviders:
    """Test suite for ProviderCoordinator.list_providers() method."""

    def test_list_providers_with_single_provider_should_return_provider_info_list(
        self, single_provider_coordinator: ProviderCoordinator
    ):
        """Should return list with single provider info."""
        provider_infos = single_provider_coordinator.list_providers()
        assert isinstance(provider_infos, list)
        assert len(provider_infos) == 1
        assert isinstance(provider_infos[0], ExternalProviderInfo)
        assert provider_infos[0].name == "mockprovider"

    def test_list_providers_with_multiple_providers_should_return_all_provider_infos(
        self, multiple_providers_coordinator: ProviderCoordinator
    ):
        """Should return list with all provider infos when multiple providers exist."""
        provider_infos = multiple_providers_coordinator.list_providers()
        assert isinstance(provider_infos, list)
        assert len(provider_infos) == 3

        provider_names = [info.name for info in provider_infos]
        assert "mockprovider1" in provider_names
        assert "mockprovider2" in provider_names
        assert "nouploadprovider" in provider_names

        # Verify all items are ExternalProviderInfo instances
        for info in provider_infos:
            assert isinstance(info, ExternalProviderInfo)

    def test_list_providers_with_no_providers_should_return_empty_list(
        self, empty_provider_coordinator: ProviderCoordinator
    ):
        """Should return empty list when no providers are registered."""
        provider_infos = empty_provider_coordinator.list_providers()
        assert isinstance(provider_infos, list)
        assert len(provider_infos) == 0


class TestProviderCoordinatorGetProvidersByCapability:
    """Test suite for ProviderCoordinator.get_providers_by_capability() method."""

    def test_get_providers_by_capability_fetch_latest_should_return_all_providers(
        self, multiple_providers_coordinator: ProviderCoordinator
    ):
        """Should return all providers that support FETCH_LATEST capability."""
        providers = multiple_providers_coordinator.get_providers_by_capability(ExternalProviderCapability.FETCH_LATEST)
        assert isinstance(providers, list)
        assert len(providers) == 3  # All providers support FETCH_LATEST

        provider_names = [provider.info.name for provider in providers]
        assert "mockprovider1" in provider_names
        assert "mockprovider2" in provider_names
        assert "nouploadprovider" in provider_names

    def test_get_providers_by_capability_upload_should_return_only_providers_with_upload(
        self, multiple_providers_coordinator: ProviderCoordinator
    ):
        """Should return only providers that support UPLOAD capability."""
        providers = multiple_providers_coordinator.get_providers_by_capability(ExternalProviderCapability.UPLOAD)
        assert isinstance(providers, list)
        assert len(providers) == 2  # Only mockprovider1 and mockprovider2 support UPLOAD

        provider_names = [provider.info.name for provider in providers]
        assert "mockprovider1" in provider_names
        assert "mockprovider2" in provider_names
        assert "nouploadprovider" not in provider_names

    def test_get_providers_by_capability_with_no_matching_providers_should_return_empty_list(
        self, single_provider_coordinator: ProviderCoordinator
    ):
        """Should return empty list when no providers support the requested capability."""
        # Create a coordinator with only fetch-only providers
        fetch_only_provider = create_mock_provider_fetch_only("fetchonly")
        registry = create_mock_registry([fetch_only_provider])
        coordinator = ProviderCoordinator(provider_registry=registry)

        providers = coordinator.get_providers_by_capability(ExternalProviderCapability.UPLOAD)
        assert isinstance(providers, list)
        assert len(providers) == 0

    def test_get_providers_by_capability_with_no_providers_should_return_empty_list(
        self, empty_provider_coordinator: ProviderCoordinator
    ):
        """Should return empty list when no providers are registered."""
        providers = empty_provider_coordinator.get_providers_by_capability(ExternalProviderCapability.FETCH_LATEST)
        assert isinstance(providers, list)
        assert len(providers) == 0

    @pytest.mark.parametrize(
        "capability,expected_count",
        [
            (ExternalProviderCapability.FETCH_LATEST, 3),
            (ExternalProviderCapability.FETCH_BY_USER, 3),
            (ExternalProviderCapability.FETCH_BY_TAGS, 3),
            (ExternalProviderCapability.UPLOAD, 2),
        ],
        ids=["fetch_latest", "fetch_by_user", "fetch_by_tags", "upload"],
    )
    def test_get_providers_by_capability_with_various_capabilities_should_return_correct_counts(
        self, multiple_providers_coordinator: ProviderCoordinator, capability, expected_count
    ):
        """Should return correct number of providers for various capabilities."""
        providers = multiple_providers_coordinator.get_providers_by_capability(capability)
        assert len(providers) == expected_count
