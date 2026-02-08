from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotUploadMediaToMultipleWithInvalidProviderNameException(DomainException):
    message: str = "Cannot upload media to multiple providers with invalid provider name"
