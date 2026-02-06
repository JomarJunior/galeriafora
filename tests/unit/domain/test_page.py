import pytest

from galeriafora import Page
from galeriafora.domain.exceptions import (
    CannotCreatePageWithHasMoreTrueButNoNextCursorException,
    CannotCreatePageWithNextCursorSetButNoMoreItemsException,
    CannotCreatePageWithNonBooleanHasMoreException,
    CannotCreatePageWithNonListItemsException,
    CannotCreatePageWithNonStringNextCursorException,
)


class TestPage:
    def test_can_be_created_with_valid_data(self):
        page = Page[int](
            items=[1, 2, 3],
            next_cursor="4",
            has_more=True,
        )
        assert page.items == [1, 2, 3]
        assert page.next_cursor == "4"
        assert page.has_more is True

    def test_str_representation(self):
        page = Page[int](
            items=[1, 2, 3],
            next_cursor="4",
            has_more=True,
        )
        expected_str = "Page(items=[1, 2, 3], next_cursor='4', has_more=True)"
        assert str(page) == expected_str

    def test_repr_representation(self):
        page = Page[int](
            items=[1, 2, 3],
            next_cursor="4",
            has_more=True,
        )
        expected_repr = "Page(items=[1, 2, 3], next_cursor='4', has_more=True)"
        assert repr(page) == expected_repr

    def test_equality(self):
        page1 = Page[int](
            items=[1, 2, 3],
            next_cursor="4",
            has_more=True,
        )
        page2 = Page[int](
            items=[1, 2, 3],
            next_cursor="4",
            has_more=True,
        )
        page3 = Page[int](
            items=[4, 5, 6],
            next_cursor="7",
            has_more=False,
        )
        assert page1 == page2
        assert page1 != page3

    def test_immutability(self):
        page = Page[int](
            items=[1, 2, 3],
            next_cursor="4",
            has_more=True,
        )
        with pytest.raises(AttributeError):
            page.items.append(4)
        with pytest.raises(AttributeError):
            page.next_cursor = "5"
        with pytest.raises(AttributeError):
            page.has_more = False

    def test_can_be_created_with_string_items(self):
        page = Page[str](
            items=["a", "b", "c"],
            next_cursor="d",
            has_more=False,
        )
        assert page.items == ["a", "b", "c"]
        assert page.next_cursor == "d"
        assert page.has_more is False

    def test_can_be_created_with_empty_items(self):
        page = Page[int](
            items=[],
            next_cursor=None,
            has_more=False,
        )
        assert page.items == []
        assert page.next_cursor is None
        assert page.has_more is False

    def test_can_be_created_with_none_next_cursor(self):
        page = Page[int](
            items=[1, 2, 3],
            next_cursor=None,
            has_more=False,
        )
        assert page.items == [1, 2, 3]
        assert page.next_cursor is None
        assert page.has_more is False

    def test_creation_with_next_cursor_but_has_more_false_should_raise_error(self):
        with pytest.raises(CannotCreatePageWithNextCursorSetButNoMoreItemsException):
            Page[int](
                items=[1, 2, 3],
                next_cursor="4",
                has_more=False,
            )

    def test_creation_with_has_more_true_but_no_next_cursor_should_raise_error(self):
        with pytest.raises(CannotCreatePageWithHasMoreTrueButNoNextCursorException):
            Page[int](
                items=[1, 2, 3],
                next_cursor=None,
                has_more=True,
            )

    def test_can_be_created_with_different_item_types(self):
        page = Page[float](
            items=[1.1, 2.2, 3.3],
            next_cursor="4.4",
            has_more=True,
        )
        assert page.items == [1.1, 2.2, 3.3]
        assert page.next_cursor == "4.4"
        assert page.has_more is True

        page = Page[dict](
            items=[{"id": 1}, {"id": 2}, {"id": 3}],
            next_cursor="4",
            has_more=True,
        )
        assert page.items == [{"id": 1}, {"id": 2}, {"id": 3}]
        assert page.next_cursor == "4"
        assert page.has_more is True

    def test_can_be_created_with_nested_page_items(self):
        inner_page1 = Page[int](items=[1, 2], next_cursor="3", has_more=True)
        inner_page2 = Page[int](items=[3, 4], next_cursor=None, has_more=False)
        page = Page[Page[int]](
            items=[inner_page1, inner_page2],
            next_cursor="5",
            has_more=True,
        )
        assert page.items == [inner_page1, inner_page2]
        assert page.next_cursor == "5"
        assert page.has_more is True

    def test_creation_with_non_string_next_cursor_should_raise_error(self):
        with pytest.raises(CannotCreatePageWithNonStringNextCursorException):
            Page[int](
                items=[1, 2, 3],
                next_cursor=4,
                has_more=True,
            )

    def test_creation_with_non_boolean_has_more_should_raise_error(self):
        with pytest.raises(CannotCreatePageWithNonBooleanHasMoreException):
            Page[int](
                items=[1, 2, 3],
                next_cursor="4",
                has_more="true",
            )

    def test_creation_with_non_list_items_should_raise_error(self):
        with pytest.raises(CannotCreatePageWithNonListItemsException):
            Page[int](
                items="not a list",
                next_cursor="4",
                has_more=True,
            )

    def test_can_be_serialized(self):
        page = Page[int](
            items=[1, 2, 3],
            next_cursor="4",
            has_more=True,
        )
        serialized = page.to_dict()
        assert serialized == {
            "items": [1, 2, 3],
            "next_cursor": "4",
            "has_more": True,
        }

    def test_can_be_deserialized(self):
        data = {
            "items": [1, 2, 3],
            "next_cursor": "4",
            "has_more": True,
        }
        page = Page[int].from_dict(data)
        assert page.items == [1, 2, 3]
        assert page.next_cursor == "4"
        assert page.has_more is True
