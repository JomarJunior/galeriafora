from galeriafora.domain.exceptions import (
    CannotCreateProviderNameThatNormalizesToEmptyException,
    CannotCreateProviderNameWithEmptyNameException,
    CannotCreateProviderNameWithNonStringNameException,
)


class ProviderName:
    _name: str

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise CannotCreateProviderNameWithNonStringNameException("Provider name must be a string.")

        if not name.strip():
            raise CannotCreateProviderNameWithEmptyNameException("Provider name cannot be empty or whitespace.")

        normalized_name = "".join(char for char in name.strip().lower() if char.isalnum())

        if not normalized_name:
            raise CannotCreateProviderNameThatNormalizesToEmptyException(
                "Provider name cannot be empty or contain only non-alphanumeric characters."
            )

        self._name = normalized_name

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self._name

    def __repr__(self):
        return f"ProviderName('{self._name}')"

    def __eq__(self, other):
        if isinstance(other, ProviderName):
            return self._name == other._name
        if isinstance(other, str):
            return self._name == other.strip().lower()
        return False
