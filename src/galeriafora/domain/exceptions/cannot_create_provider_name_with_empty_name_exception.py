from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotCreateProviderNameWithEmptyNameException(DomainException):
    message: str = "Cannot create a ProviderName with an empty name."
