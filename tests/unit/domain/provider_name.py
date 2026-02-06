import pytest

from galeriafora import ProviderName
from galeriafora.domain.exceptions import (
    CannotCreateProviderNameThatNormalizesToEmptyException,
    CannotCreateProviderNameWithEmptyNameException,
    CannotCreateProviderNameWithNonStringNameException,
    CannotCreateProviderNameWithOnlyNonAlphanumericCharactersException,
)


class TestProviderName:
    def test_can_be_created_with_valid_name(self):
        name = "exampleprovider"
        provider_name = ProviderName(name)
        assert provider_name.name == name

    def test_str_representation(self):
        name = "exampleprovider"
        provider_name = ProviderName(name)
        assert str(provider_name) == name

    def test_equality(self):
        name1 = "exampleprovider"
        name2 = "exampleprovider"
        name3 = "anotherprovider"
        provider_name1 = ProviderName(name1)
        provider_name2 = ProviderName(name2)
        provider_name3 = ProviderName(name3)
        assert provider_name1 == provider_name2
        assert provider_name1 != provider_name3

    def test_it_normalizes_name_to_lowercase(self):
        name = "ExampleProvider"
        provider_name = ProviderName(name)
        assert provider_name.name == "exampleprovider"

    def test_it_strips_whitespace_from_name(self):
        name = "  exampleprovider  "
        provider_name = ProviderName(name)
        assert provider_name.name == "exampleprovider"

    def test_it_strips_non_alphanumeric_characters_from_name(self):
        name = "example provider!@#"
        provider_name = ProviderName(name)
        assert provider_name.name == "exampleprovider"

    def test_immutability(self):
        provider_name = ProviderName("immutableprovider")
        with pytest.raises(AttributeError):
            provider_name.name = "newname"

    def test_creation_with_empty_name_should_raise_error(self):
        with pytest.raises(CannotCreateProviderNameWithEmptyNameException):
            ProviderName("")

    def test_creation_with_whitespace_name_should_raise_error(self):
        with pytest.raises(CannotCreateProviderNameWithEmptyNameException):
            ProviderName("   ")

    def test_creation_with_non_string_name_should_raise_error(self):
        with pytest.raises(TypeError):
            ProviderName(123)

    def test_creation_with_name_with_only_non_alphanumeric_characters_should_raise_error(self):
        with pytest.raises(CannotCreateProviderNameWithEmptyNameException):
            ProviderName("!@#$%^&*()")

    def test_creation_with_name_that_normalizes_to_empty_should_raise_error(self):
        with pytest.raises(CannotCreateProviderNameWithEmptyNameException):
            ProviderName("   !@#$%^&*()   ")

    def test_creation_with_name_that_normalizes_to_valid_name(self):
        provider_name = ProviderName("  Example Provider!@#  ")
        assert provider_name.name == "exampleprovider"

    def test_equality_with_different_cases_and_whitespace(self):
        provider_name1 = ProviderName("  ExampleProvider  ")
        provider_name2 = ProviderName("exampleprovider")
        provider_name3 = ProviderName("EXAMPLEPROVIDER")
        assert provider_name1 == provider_name2
        assert provider_name1 == provider_name3
        assert provider_name2 == provider_name3

    def test_equality_with_different_names(self):
        provider_name1 = ProviderName("ExampleProvider")
        provider_name2 = ProviderName("AnotherProvider")
        assert provider_name1 != provider_name2

    def test_can_be_assimilated_from_string(self):
        class CustomClass:
            def __init__(self, provider_name: ProviderName):
                self.provider_name = provider_name

        custom_instance = CustomClass(provider_name="ExampleProvider")
        assert custom_instance.provider_name == ProviderName("ExampleProvider")

    def test_str_equality(self):
        provider_name = ProviderName("ExampleProvider")
        assert provider_name == "exampleprovider"
        assert provider_name == "ExampleProvider"
        assert provider_name == "EXAMPLEPROVIDER"
        assert provider_name != "anotherprovider"
