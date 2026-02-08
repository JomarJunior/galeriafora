from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotFetchMediaByUserWithInvalidProviderNameException(DomainException):
    message: str = "Cannot fetch media by user with invalid provider name"
