from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotUploadMediaToMultipleWithoutRegisteredProvidersException(DomainException):
    message: str = "Cannot upload media to multiple providers without registered providers"
