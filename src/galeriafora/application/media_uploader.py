"""
MediaUploader application service for orchestrating media upload operations.

This service coordinates with the IProviderRegistry and IExternalProvider interface
to upload media to external providers, following hexagonal architecture principles.
"""

from typing import Dict, Sequence

from galeriafora.domain import (
    ExternalMedia,
    ExternalProviderCapability,
    IExternalProvider,
    IProviderRegistry,
    ProviderName,
)
from galeriafora.domain.exceptions import (
    CannotInitializeMediaUploaderWithInvalidProviderRegistryException,
    CannotUploadMediaProviderDoesNotSupportUploadException,
    CannotUploadMediaToMultipleWithInvalidProviderNameException,
    CannotUploadMediaToMultipleWithoutRegisteredProvidersException,
    CannotUploadMediaWithInvalidProviderNameException,
    CannotUploadMediaWithoutRegisteredProvidersException,
)


class MediaUploader:
    """
    Application service for orchestrating media upload operations.

    Coordinates with registered providers to upload media while respecting
    provider capabilities.
    """

    def __init__(self, provider_registry: IProviderRegistry):
        """
        Initialize MediaUploader with a provider registry.

        Args:
            provider_registry: The registry containing all available providers.

        Raises:
            CannotInitializeMediaUploaderWithInvalidProviderRegistryException:
                If provider_registry is None or not a IProviderRegistry instance.
        """
        if provider_registry is None or not isinstance(provider_registry, IProviderRegistry):
            raise CannotInitializeMediaUploaderWithInvalidProviderRegistryException()

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

    async def upload(self, provider_name: str, media: ExternalMedia) -> bool:
        """
        Upload media to a provider.

        Args:
            provider_name: The name of the provider to upload to.
            media: The media to upload.

        Returns:
            bool: True if upload was successful, False otherwise.

        Raises:
            CannotUploadMediaWithoutRegisteredProvidersException:
                If no providers are registered.
            CannotUploadMediaWithInvalidProviderNameException:
                If provider_name is invalid (None or empty string).
            CannotUploadMediaProviderDoesNotSupportUploadException:
                If the provider doesn't support the UPLOAD capability.
        """
        # Check if providers are registered
        if not self.provider_registry.get_providers():
            raise CannotUploadMediaWithoutRegisteredProvidersException("No providers are registered")

        # Validate provider name
        if not provider_name or not isinstance(provider_name, str):
            raise CannotUploadMediaWithInvalidProviderNameException("provider_name must be a non-empty string")

        # Get the provider
        try:
            provider = self._get_provider(provider_name)
        except (ValueError, KeyError) as e:
            raise CannotUploadMediaWithInvalidProviderNameException() from e

        # Check if provider supports UPLOAD capability
        if not provider.info.has_capability(ExternalProviderCapability.UPLOAD):
            raise CannotUploadMediaProviderDoesNotSupportUploadException(
                f"Provider '{provider_name}' does not support UPLOAD capability"
            )

        # Upload and return result
        try:
            await provider.upload([media])
        except Exception:
            # Log the exception if needed
            return False
        return True

    async def upload_to_multiple(self, media: ExternalMedia, providers: Sequence[str]) -> Dict[str, bool]:
        """
        Upload media to multiple providers.

        Args:
            media: The media to upload.
            providers: A sequence of provider names to upload to.

        Returns:
            Dict[str, bool]: A dictionary mapping provider names to upload results.

        Raises:
            CannotUploadMediaToMultipleWithoutRegisteredProvidersException:
                If no providers are registered.
            CannotUploadMediaToMultipleWithInvalidProviderNameException:
                If any provider_name is invalid (None or empty string).
            CannotUploadMediaProviderDoesNotSupportUploadException:
                If any provider doesn't support the UPLOAD capability.
        """
        # Check if providers are registered
        if not self.provider_registry.get_providers():
            raise CannotUploadMediaToMultipleWithoutRegisteredProvidersException("No providers are registered")

        results: Dict[str, bool] = {}

        # Process each provider
        for provider_name in providers:
            # Validate provider name
            if not provider_name or not isinstance(provider_name, str):
                raise CannotUploadMediaToMultipleWithInvalidProviderNameException(
                    "provider_name must be a non-empty string"
                )

            # Get the provider
            try:
                provider = self._get_provider(provider_name)
            except (ValueError, KeyError) as e:
                raise CannotUploadMediaToMultipleWithInvalidProviderNameException() from e

            # Check if provider supports UPLOAD capability
            if not provider.info.has_capability(ExternalProviderCapability.UPLOAD):
                raise CannotUploadMediaProviderDoesNotSupportUploadException(
                    f"Provider '{provider_name}' does not support UPLOAD capability"
                )

            # Upload to this provider
            try:
                await provider.upload([media])
                results[provider_name] = True
            except Exception:
                # Log the exception if needed
                results[provider_name] = False

        return results
