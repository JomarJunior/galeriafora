from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotFetchLatestMediaProviderDoesNotSupportFetchLatestException(DomainException):
    message: str = "Cannot fetch latest media: provider does not support FETCH_LATEST"
