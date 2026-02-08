from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotCreatePageWithNonBooleanHasMoreException(DomainException):
    message: str = "Cannot create a Page with a non-boolean has_more value."
