from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotCreateProviderNameWithNonStringNameException(DomainException):
    message: str = "Cannot create a ProviderName with a non-string name."
