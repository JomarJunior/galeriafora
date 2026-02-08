from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotUploadMediaWithoutRegisteredProvidersException(DomainException):
    message: str = "Cannot upload media without registered providers"
