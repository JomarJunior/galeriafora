from galeriafora.domain.exceptions.cannot_create_external_media_with_description_exceeding_max_length_exception import (
    CannotCreateExternalMediaWithDescriptionExceedingMaxLengthException,
)
from galeriafora.domain.exceptions.cannot_create_external_media_with_empty_title_exception import (
    CannotCreateExternalMediaWithEmptyTitleException,
)
from galeriafora.domain.exceptions.cannot_create_external_media_with_invalid_content_metadata_exception import (
    CannotCreateExternalMediaWithInvalidContentMetadataException,
)
from galeriafora.domain.exceptions.cannot_create_external_media_with_invalid_provider_exception import (
    CannotCreateExternalMediaWithInvalidProviderException,
)
from galeriafora.domain.exceptions.cannot_create_external_media_with_invalid_rating_exception import (
    CannotCreateExternalMediaWithInvalidRatingException,
)
from galeriafora.domain.exceptions.cannot_create_external_media_with_invalid_url_exception import (
    CannotCreateExternalMediaWithInvalidURLException,
)
from galeriafora.domain.exceptions.cannot_create_external_media_with_title_exceeding_max_length_exception import (
    CannotCreateExternalMediaWithTitleExceedingMaxLengthException,
)
from galeriafora.domain.exceptions.cannot_create_external_media_with_too_many_tags_exception import (
    CannotCreateExternalMediaWithTooManyTagsException,
)
from galeriafora.domain.exceptions.cannot_create_external_provider_info_with_empty_capabilities_exception import (
    CannotCreateExternalProviderInfoWithEmptyCapabilitiesException,
)
from galeriafora.domain.exceptions.cannot_create_external_provider_info_with_empty_name_exception import (
    CannotCreateExternalProviderInfoWithEmptyNameException,
)
from galeriafora.domain.exceptions.cannot_create_external_provider_info_with_invalid_capabilities_exception import (
    CannotCreateExternalProviderInfoWithInvalidCapabilitiesException,
)
from galeriafora.domain.exceptions.cannot_create_page_with_has_more_true_but_no_next_cursor_exception import (
    CannotCreatePageWithHasMoreTrueButNoNextCursorException,
)
from galeriafora.domain.exceptions.cannot_create_page_with_next_cursor_set_but_no_more_items_exception import (
    CannotCreatePageWithNextCursorSetButNoMoreItemsException,
)
from galeriafora.domain.exceptions.cannot_create_page_with_non_boolean_has_more_exception import (
    CannotCreatePageWithNonBooleanHasMoreException,
)
from galeriafora.domain.exceptions.cannot_create_page_with_non_list_items_exception import (
    CannotCreatePageWithNonListItemsException,
)
from galeriafora.domain.exceptions.cannot_create_page_with_non_string_next_cursor_exception import (
    CannotCreatePageWithNonStringNextCursorException,
)
from galeriafora.domain.exceptions.cannot_create_provider_name_that_normalizes_to_empty_exception import (
    CannotCreateProviderNameThatNormalizesToEmptyException,
)
from galeriafora.domain.exceptions.cannot_create_provider_name_with_empty_name_exception import (
    CannotCreateProviderNameWithEmptyNameException,
)
from galeriafora.domain.exceptions.cannot_create_provider_name_with_non_string_name_exception import (
    CannotCreateProviderNameWithNonStringNameException,
)

__all__ = [
    "CannotCreateProviderNameThatNormalizesToEmptyException",
    "CannotCreateProviderNameWithEmptyNameException",
    "CannotCreateProviderNameWithNonStringNameException",
    "CannotCreatePageWithHasMoreTrueButNoNextCursorException",
    "CannotCreatePageWithNextCursorSetButNoMoreItemsException",
    "CannotCreatePageWithNonBooleanHasMoreException",
    "CannotCreatePageWithNonListItemsException",
    "CannotCreatePageWithNonStringNextCursorException",
    "CannotCreateExternalProviderInfoWithEmptyCapabilitiesException",
    "CannotCreateExternalProviderInfoWithEmptyNameException",
    "CannotCreateExternalProviderInfoWithInvalidCapabilitiesException",
    "CannotCreateExternalMediaWithInvalidURLException",
    "CannotCreateExternalMediaWithTitleExceedingMaxLengthException",
    "CannotCreateExternalMediaWithTooManyTagsException",
    "CannotCreateExternalMediaWithDescriptionExceedingMaxLengthException",
    "CannotCreateExternalMediaWithEmptyTitleException",
    "CannotCreateExternalMediaWithInvalidProviderException",
    "CannotCreateExternalMediaWithInvalidContentMetadataException",
    "CannotCreateExternalMediaWithInvalidRatingException",
]
