"""
Provider Registry interface for managing external providers.

This interface defines the contract for discovering and retrieving providers,
following hexagonal architecture principles.
"""

from abc import ABC, abstractmethod
from typing import Sequence

from galeriafora.domain.i_external_provider import IExternalProvider


class IProviderRegistry(ABC):
    """Abstract interface for managing and retrieving registered providers."""

    @abstractmethod
    def get_providers(self) -> Sequence[IExternalProvider]:
        """
        Retrieve all registered providers.

        Returns:
            Sequence[IExternalProvider]: A sequence of all registered providers.
        """
