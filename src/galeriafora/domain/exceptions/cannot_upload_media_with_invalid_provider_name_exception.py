from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotUploadMediaWithInvalidProviderNameException(DomainException):
    message: str = "Cannot upload media with invalid provider name"
