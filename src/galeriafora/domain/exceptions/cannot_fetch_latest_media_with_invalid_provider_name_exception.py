from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotFetchLatestMediaWithInvalidProviderNameException(DomainException):
    message: str = "Cannot fetch latest media with invalid provider name"
