from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotCreateExternalMediaWithDescriptionExceedingMaxLengthException(DomainException):
    message: str = "Cannot create an ExternalMedia with a description exceeding the maximum allowed length."
