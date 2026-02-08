"""
MediaFetcher application service for orchestrating media fetching operations.

This service coordinates with the ProviderRegistry and IExternalProvider interface
to fetch media from external providers, following hexagonal architecture principles.
"""

from typing import Optional, Sequence

from galeriafora.domain import (
    ExternalProviderCapability,
    IExternalProvider,
    IProviderRegistry,
    Page,
    ProviderName,
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

# Default limit per architecture documentation
DEFAULT_LIMIT = 200


class MediaFetcher:
    """
    Application service for orchestrating media fetching operations.

    Coordinates with registered providers to fetch media based on various criteria
    (latest, by user, by tags) while respecting provider capabilities.
    """

    def __init__(self, provider_registry: IProviderRegistry):
        """
        Initialize MediaFetcher with a provider registry.

        Args:
            provider_registry: The registry containing all available providers.

        Raises:
            CannotInitializeMediaFetcherWithInvalidProviderRegistryException:
                If provider_registry is None or not a ProviderRegistry instance.
        """
        if provider_registry is None or not isinstance(provider_registry, IProviderRegistry):
            raise CannotInitializeMediaFetcherWithInvalidProviderRegistryException()

        self.provider_registry = provider_registry

    def _get_provider(self, provider_name: str) -> IExternalProvider:
        """
        Retrieve a provider by name from the registry.

        Args:
            provider_name: The name of the provider to retrieve.

        Returns:
            IExternalProvider: The provider matching the given name.

        Raises:
            ValueError: If provider_name is None or empty.
            KeyError: If provider is not found in registry.
        """
        if not provider_name or not isinstance(provider_name, str):
            raise ValueError("provider_name must be a non-empty string")

        # Normalize the provider name for comparison
        normalized_name = ProviderName(provider_name)

        providers = self.provider_registry.get_providers()
        for provider in providers:
            if provider.info.name == normalized_name:
                return provider

        raise KeyError(f"Provider '{provider_name}' not found in registry")

    async def fetch_latest(self, provider_name: str, limit: int = DEFAULT_LIMIT) -> Page:
        """
        Fetch latest media from a provider.

        Args:
            provider_name: The name of the provider to fetch from.
            limit: The maximum number of items to fetch (default: 200).

        Returns:
            Page: A page containing the fetched media.

        Raises:
            CannotFetchLatestMediaWithoutRegisteredProvidersException:
                If no providers are registered.
            CannotFetchLatestMediaWithInvalidProviderNameException:
                If provider_name is invalid (None or empty string).
            CannotFetchLatestMediaProviderDoesNotSupportFetchLatestException:
                If the provider doesn't support the FETCH_LATEST capability.
        """
        # Check if providers are registered
        if not self.provider_registry.get_providers():
            raise CannotFetchLatestMediaWithoutRegisteredProvidersException()

        # Validate provider name
        if not provider_name or not isinstance(provider_name, str):
            raise CannotFetchLatestMediaWithInvalidProviderNameException()

        # Get the provider
        try:
            provider = self._get_provider(provider_name)
        except (ValueError, KeyError) as e:
            raise CannotFetchLatestMediaWithInvalidProviderNameException() from e

        # Check if provider supports FETCH_LATEST capability
        if not provider.info.has_capability(ExternalProviderCapability.FETCH_LATEST):
            raise CannotFetchLatestMediaProviderDoesNotSupportFetchLatestException()

        # Fetch and return media
        return await provider.fetch_latest(limit=limit)

    async def fetch_by_user(self, provider_name: str, username: str, limit: int = DEFAULT_LIMIT) -> Page:
        """
        Fetch media by user from a provider.

        Args:
            provider_name: The name of the provider to fetch from.
            username: The username to fetch media for.
            limit: The maximum number of items to fetch (default: 200).

        Returns:
            Page: A page containing the fetched media.

        Raises:
            CannotFetchMediaByUserWithoutRegisteredProvidersException:
                If no providers are registered.
            CannotFetchMediaByUserWithInvalidProviderNameException:
                If provider_name is invalid (None or empty string).
            CannotFetchMediaByUserProviderDoesNotSupportFetchByUserException:
                If the provider doesn't support the FETCH_BY_USER capability.
        """
        # Check if providers are registered
        if not self.provider_registry.get_providers():
            raise CannotFetchMediaByUserWithoutRegisteredProvidersException()

        # Validate provider name
        if not provider_name or not isinstance(provider_name, str):
            raise CannotFetchMediaByUserWithInvalidProviderNameException()

        # Get the provider
        try:
            provider = self._get_provider(provider_name)
        except (ValueError, KeyError) as e:
            raise CannotFetchMediaByUserWithInvalidProviderNameException() from e

        # Check if provider supports FETCH_BY_USER capability
        if not provider.info.has_capability(ExternalProviderCapability.FETCH_BY_USER):
            raise CannotFetchMediaByUserProviderDoesNotSupportFetchByUserException()

        # Fetch and return media
        return await provider.fetch_by_user(username, limit=limit)

    async def fetch_by_tags(
        self, provider_name: str, tags: Optional[Sequence[str]], limit: int = DEFAULT_LIMIT
    ) -> Page:
        """
        Fetch media by tags from a provider.

        Args:
            provider_name: The name of the provider to fetch from.
            tags: The tags to search for.
            limit: The maximum number of items to fetch (default: 200).

        Returns:
            Page: A page containing the fetched media.

        Raises:
            CannotFetchMediaByTagsWithoutRegisteredProvidersException:
                If no providers are registered.
            CannotFetchMediaByTagsWithInvalidProviderNameException:
                If provider_name is invalid (None or empty string).
            CannotFetchMediaByTagsProviderDoesNotSupportFetchByTagsException:
                If the provider doesn't support the FETCH_BY_TAGS capability.
        """
        # Check if providers are registered
        if not self.provider_registry.get_providers():
            raise CannotFetchMediaByTagsWithoutRegisteredProvidersException()

        # Validate provider name
        if not provider_name or not isinstance(provider_name, str):
            raise CannotFetchMediaByTagsWithInvalidProviderNameException()

        # Get the provider
        try:
            provider = self._get_provider(provider_name)
        except (ValueError, KeyError) as e:
            raise CannotFetchMediaByTagsWithInvalidProviderNameException() from e

        # Check if provider supports FETCH_BY_TAGS capability
        if not provider.info.has_capability(ExternalProviderCapability.FETCH_BY_TAGS):
            raise CannotFetchMediaByTagsProviderDoesNotSupportFetchByTagsException()

        # Fetch and return media
        return await provider.fetch_by_tags(tags or [], limit=limit)
