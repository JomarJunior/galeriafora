from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotFetchMediaByUserWithoutRegisteredProvidersException(DomainException):
    message: str = "Cannot fetch media by user without registered providers"
