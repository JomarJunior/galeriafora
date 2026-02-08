from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotUploadMediaProviderDoesNotSupportUploadException(DomainException):
    message: str = "Cannot upload media because the provider does not support upload"
