import pytest

from galeriafora import ExternalProviderCapability


class TestExternalProviderCapability:
    def test_external_provider_capability_enum(self):
        assert ExternalProviderCapability.FETCH_LATEST.value == "fetch_latest"
        assert ExternalProviderCapability.FETCH_BY_USER.value == "fetch_by_user"
        assert ExternalProviderCapability.FETCH_BY_TAGS.value == "fetch_by_tags"
        assert ExternalProviderCapability.UPLOAD.value == "upload"

    def test_str_representation(self):
        for capability in ExternalProviderCapability.__members__.values():
            assert str(capability) == capability.value

    def test_equality(self):
        assert ExternalProviderCapability.FETCH_LATEST == ExternalProviderCapability.FETCH_LATEST
        assert ExternalProviderCapability.FETCH_LATEST != ExternalProviderCapability.FETCH_BY_USER
        assert ExternalProviderCapability.FETCH_BY_USER == ExternalProviderCapability.FETCH_BY_USER
        assert ExternalProviderCapability.FETCH_BY_USER != ExternalProviderCapability.FETCH_BY_TAGS
        assert ExternalProviderCapability.FETCH_BY_TAGS == ExternalProviderCapability.FETCH_BY_TAGS
        assert ExternalProviderCapability.FETCH_BY_TAGS != ExternalProviderCapability.UPLOAD
        assert ExternalProviderCapability.UPLOAD == ExternalProviderCapability.UPLOAD
        assert ExternalProviderCapability.UPLOAD != ExternalProviderCapability.FETCH_LATEST

    def test_can_be_created_from_string(self):
        assert ExternalProviderCapability("fetch_latest") == ExternalProviderCapability.FETCH_LATEST
        assert ExternalProviderCapability("fetch_by_user") == ExternalProviderCapability.FETCH_BY_USER
        assert ExternalProviderCapability("fetch_by_tags") == ExternalProviderCapability.FETCH_BY_TAGS
        assert ExternalProviderCapability("upload") == ExternalProviderCapability.UPLOAD

    def test_string_equality(self):
        assert ExternalProviderCapability.FETCH_LATEST == "fetch_latest"
        assert ExternalProviderCapability.FETCH_BY_USER == "fetch_by_user"
        assert ExternalProviderCapability.FETCH_BY_TAGS == "fetch_by_tags"
        assert ExternalProviderCapability.UPLOAD == "upload"

    def test_can_be_assimilated_from_string(self):
        class CustomClass:
            def __init__(self, capability: ExternalProviderCapability):
                self.capability = capability

        custom_instance = CustomClass(capability="fetch_latest")
        assert custom_instance.capability == ExternalProviderCapability.FETCH_LATEST

    def test_repr_returns_enum_value(self):
        capability = ExternalProviderCapability.FETCH_BY_USER
        assert repr(capability) == "fetch_by_user"
        assert repr(capability) == "fetch_by_user"
