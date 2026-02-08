from enum import Enum


class ExternalProviderCapability(str, Enum):
    FETCH_LATEST = "fetch_latest"
    FETCH_BY_USER = "fetch_by_user"
    FETCH_BY_TAGS = "fetch_by_tags"
    UPLOAD = "upload"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value
