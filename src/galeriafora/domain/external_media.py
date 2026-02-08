import urllib.parse
from typing import List, Optional

from galeriafora.domain.ai_metadata import AiMetadata
from galeriafora.domain.content_metadata import ContentMetadata
from galeriafora.domain.exceptions import (
    CannotCreateExternalMediaWithEmptyTitleException,
    CannotCreateExternalMediaWithInvalidContentMetadataException,
    CannotCreateExternalMediaWithInvalidProviderException,
    CannotCreateExternalMediaWithInvalidURLException,
    CannotCreateExternalMediaWithTitleExceedingMaxLengthException,
    CannotCreateExternalMediaWithTooManyTagsException,
)
from galeriafora.domain.exceptions.cannot_create_external_media_with_description_exceeding_max_length_exception import (
    CannotCreateExternalMediaWithDescriptionExceedingMaxLengthException,
)
from galeriafora.domain.external_provider_info import ExternalProviderInfo
from galeriafora.domain.mature_rating import MatureRating


class ExternalMedia:
    def __init__(
        self,
        url: str,
        title: str,
        description: str,
        content_metadata: ContentMetadata,
        tags: List[str],
        mature_rating: MatureRating,
        ai_metadata: Optional[AiMetadata],
        provider: ExternalProviderInfo,
    ):
        if not url or not isinstance(url, str) or not self._is_valid_url(url):
            raise CannotCreateExternalMediaWithInvalidURLException()

        if not title or not isinstance(title, str) or title.strip() == "":
            raise CannotCreateExternalMediaWithEmptyTitleException()

        if len(title) > 255:
            raise CannotCreateExternalMediaWithTitleExceedingMaxLengthException()

        if len(description) > 2048:
            raise CannotCreateExternalMediaWithDescriptionExceedingMaxLengthException()

        if len(tags) > 30:
            raise CannotCreateExternalMediaWithTooManyTagsException()

        if not provider or not isinstance(provider, ExternalProviderInfo):
            raise CannotCreateExternalMediaWithInvalidProviderException()

        self._url = url
        self._title = title
        self._description = description
        self._content_metadata = content_metadata
        self._tags = tags
        self._mature_rating = mature_rating
        self._ai_metadata = ai_metadata
        self._provider = provider

    @property
    def url(self) -> str:
        return self._url

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def content_metadata(self) -> ContentMetadata:
        return self._content_metadata

    @property
    def tags(self) -> List[str]:
        return list(self._tags)

    @property
    def mature_rating(self) -> MatureRating:
        return self._mature_rating

    @property
    def ai_metadata(self) -> Optional[AiMetadata]:
        return self._ai_metadata

    @property
    def provider(self) -> ExternalProviderInfo:
        return self._provider

    @classmethod
    def from_dict(cls, data: dict) -> "ExternalMedia":
        return cls(
            url=data["url"],
            title=data["title"],
            description=data.get("description", ""),
            content_metadata=ContentMetadata.from_dict(data["content_metadata"]),
            tags=data.get("tags", []),
            mature_rating=MatureRating(data["mature_rating"]),
            ai_metadata=AiMetadata.from_dict(data["ai_metadata"]) if data.get("ai_metadata") else None,
            provider=ExternalProviderInfo.from_dict(data["provider"]),
        )

    def _is_valid_url(self, url: str) -> bool:
        try:
            if url.find(" ") != -1:
                return False
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def __str__(self) -> str:
        return (
            f"ExternalMedia(url={self.url}, title={self.title}, description={self.description}, "
            f"content_metadata={self.content_metadata}, tags={self.tags}, mature_rating={self.mature_rating}, "
            f"ai_metadata={self.ai_metadata}, provider={self.provider})"
        )

    def __repr__(self) -> str:
        return (
            f"ExternalMedia(url={self.url}, title={self.title}, description={self.description}, "
            f"content_metadata={self.content_metadata}, tags={self.tags}, mature_rating={self.mature_rating}, "
            f"ai_metadata={self.ai_metadata}, provider={self.provider})"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, ExternalMedia):
            return False
        return (
            self.url == other.url
            and self.title == other.title
            and self.description == other.description
            and self.content_metadata == other.content_metadata
            and self.tags == other.tags
            and self.mature_rating == other.mature_rating
            and self.ai_metadata == other.ai_metadata
            and self.provider == other.provider
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.url,
                self.title,
                self.description,
                str(self.content_metadata),
                tuple(self.tags),
                self.mature_rating,
                str(self.ai_metadata),
                str(self.provider),
            )
        )

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "content_metadata": self.content_metadata.to_dict(),
            "tags": self.tags,
            "mature_rating": self.mature_rating.value,
            "ai_metadata": self.ai_metadata.to_dict() if self.ai_metadata else None,
            "provider": self.provider.to_dict(),
        }
