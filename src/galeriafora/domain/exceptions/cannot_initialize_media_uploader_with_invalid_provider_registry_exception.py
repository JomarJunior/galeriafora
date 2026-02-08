from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotInitializeMediaUploaderWithInvalidProviderRegistryException(DomainException):
    message: str = "Cannot initialize MediaUploader with invalid provider registry"
