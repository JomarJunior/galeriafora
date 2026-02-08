from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotCreatePageWithNextCursorSetButNoMoreItemsException(DomainException):
    message: str = "Cannot create a Page with next_cursor set but has_more=False, indicating no more items."
