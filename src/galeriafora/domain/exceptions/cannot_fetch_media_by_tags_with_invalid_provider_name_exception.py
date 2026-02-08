from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotFetchMediaByTagsWithInvalidProviderNameException(DomainException):
    message: str = "Cannot fetch media by tags with invalid provider name"
