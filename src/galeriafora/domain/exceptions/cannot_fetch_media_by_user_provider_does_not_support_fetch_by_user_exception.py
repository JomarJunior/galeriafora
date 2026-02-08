from dataclasses import dataclass

from galeriafora.domain.exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class CannotFetchMediaByUserProviderDoesNotSupportFetchByUserException(DomainException):
    message: str = "Cannot fetch media by user: provider does not support FETCH_BY_USER"
