from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotCreateProviderNameThatNormalizesToEmptyException(DomainException):
    message: str = "Cannot create a ProviderName that normalizes to an empty string."
