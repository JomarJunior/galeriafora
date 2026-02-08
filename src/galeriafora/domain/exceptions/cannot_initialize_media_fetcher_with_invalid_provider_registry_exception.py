from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotInitializeMediaFetcherWithInvalidProviderRegistryException(DomainException):
    message: str = "Cannot initialize media fetcher with invalid provider registry"
