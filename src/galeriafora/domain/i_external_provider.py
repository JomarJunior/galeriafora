from abc import ABC, abstractmethod
from typing import Optional, Sequence

from galeriafora.domain.external_media import ExternalMedia
from galeriafora.domain.external_provider_info import ExternalProviderInfo
from galeriafora.domain.page import Page


class IExternalProvider(ABC):
    @property
    @abstractmethod
    def info(self) -> ExternalProviderInfo:
        """Returns the ExternalProviderInfo associated with this provider."""

    @abstractmethod
    async def fetch_latest(self, *, limit: int = 200, cursor: Optional[str] = None) -> Page:
        """Fetches the latest media items from the provider."""

    @abstractmethod
    async def fetch_by_user(
        self, username: str, *, limit: int = 200, cursor: Optional[str] = None
    ) -> Page[ExternalMedia]:
        """Fetches media items associated with a specific user."""

    @abstractmethod
    async def fetch_by_tags(
        self, tags: Sequence[str], *, limit: int = 200, cursor: Optional[str] = None
    ) -> Page[ExternalMedia]:
        """Fetches media items associated with specific tags."""

    @abstractmethod
    async def upload(self, media: Sequence[ExternalMedia]) -> None:
        """Uploads media items to the provider."""
