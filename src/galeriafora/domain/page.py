from typing import Any, Dict, Generic, List, TypeVar

from galeriafora.domain.exceptions import (
    CannotCreatePageWithHasMoreTrueButNoNextCursorException,
    CannotCreatePageWithNextCursorSetButNoMoreItemsException,
    CannotCreatePageWithNonBooleanHasMoreException,
    CannotCreatePageWithNonListItemsException,
    CannotCreatePageWithNonStringNextCursorException,
)

T = TypeVar("T")


class Page(Generic[T]):
    def __init__(self, items: List[T], next_cursor: str | None, has_more: bool):
        if not isinstance(items, list):
            raise CannotCreatePageWithNonListItemsException()
        if not isinstance(has_more, bool):
            raise CannotCreatePageWithNonBooleanHasMoreException()
        if next_cursor is not None and not isinstance(next_cursor, str):
            raise CannotCreatePageWithNonStringNextCursorException()
        if has_more and next_cursor is None:
            raise CannotCreatePageWithHasMoreTrueButNoNextCursorException()
        if not has_more and next_cursor is not None:
            raise CannotCreatePageWithNextCursorSetButNoMoreItemsException()

        self._items = tuple(items)  # Convert list to tuple for immutability
        self._next_cursor = next_cursor
        self._has_more = has_more

    @property
    def items(self) -> List[T]:
        return list(self._items)

    @property
    def next_cursor(self) -> str | None:
        return self._next_cursor

    @property
    def has_more(self) -> bool:
        return self._has_more

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Page":
        return cls(
            items=list(data.get("items", [])),
            next_cursor=data.get("next_cursor"),
            has_more=data.get("has_more", False),
        )

    def to_dict(self) -> dict:
        return {
            "items": list(self.items),
            "next_cursor": self.next_cursor,
            "has_more": self.has_more,
        }

    def __str__(self) -> str:
        return f"Page(items={self.items}, next_cursor={self.next_cursor!r}, has_more={self.has_more})"

    def __repr__(self) -> str:
        return f"Page(items={self.items}, next_cursor={self.next_cursor!r}, has_more={self.has_more})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Page):
            return False
        return self.items == other.items and self.next_cursor == other.next_cursor and self.has_more == other.has_more
