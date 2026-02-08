from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotCreateExternalMediaWithInvalidContentMetadataException(DomainException):
    message: str = "Cannot create an ExternalMedia with invalid content metadata."
