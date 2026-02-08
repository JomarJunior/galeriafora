from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotCreateExternalMediaWithInvalidRatingException(DomainException):
    message: str = "Cannot create an ExternalMedia with an invalid rating."
