from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotCreateExternalProviderInfoWithEmptyCapabilitiesException(DomainException):
    message: str = "Cannot create an ExternalProviderInfo with empty capabilities."
