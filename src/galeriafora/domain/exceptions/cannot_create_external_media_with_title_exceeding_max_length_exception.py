from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotCreateExternalMediaWithTitleExceedingMaxLengthException(DomainException):
    message: str = "Cannot create an ExternalMedia with a title exceeding the maximum allowed length."
