from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotCreatePageWithNonStringNextCursorException(DomainException):
    message: str = "Cannot create a Page with a non-string next_cursor value."
