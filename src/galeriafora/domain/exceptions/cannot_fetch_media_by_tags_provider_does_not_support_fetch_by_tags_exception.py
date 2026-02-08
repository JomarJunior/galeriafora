from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotFetchMediaByTagsProviderDoesNotSupportFetchByTagsException(DomainException):
    message: str = "Cannot fetch media by tags: provider does not support FETCH_BY_TAGS"
