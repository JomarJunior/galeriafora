from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotFetchMediaByTagsWithoutRegisteredProvidersException(DomainException):
    message: str = "Cannot fetch media by tags without registered providers"
