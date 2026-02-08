import pytest

from galeriafora import ExternalProviderCapability, ExternalProviderInfo, ProviderName
from galeriafora.domain.exceptions import (
    CannotCreateExternalProviderInfoWithEmptyCapabilitiesException,
    CannotCreateExternalProviderInfoWithInvalidCapabilitiesException,
)


class TestExternalProviderInfo:
    def test_can_be_created_with_valid_data(self):
        provider_info = ExternalProviderInfo(
            name=ProviderName("testprovider"),
            description="A test provider",
            capabilities=[
                ExternalProviderCapability.FETCH_LATEST,
                ExternalProviderCapability.FETCH_BY_USER,
                ExternalProviderCapability.FETCH_BY_TAGS,
                ExternalProviderCapability.UPLOAD,
            ],
        )

        assert provider_info.name == ProviderName("testprovider")
        assert provider_info.description == "A test provider"
        assert ExternalProviderCapability.FETCH_LATEST in provider_info.capabilities
        assert ExternalProviderCapability.FETCH_BY_USER in provider_info.capabilities
        assert ExternalProviderCapability.FETCH_BY_TAGS in provider_info.capabilities
        assert ExternalProviderCapability.UPLOAD in provider_info.capabilities

    def test_str_representation(self):
        provider_info = ExternalProviderInfo(
            name=ProviderName("strprovider"),
            description="String provider",
            capabilities=[ExternalProviderCapability.FETCH_LATEST],
        )
        expected_str = (
            "ExternalProviderInfo(name=strprovider, description='String provider', capabilities=[fetch_latest])"
        )
        assert str(provider_info) == expected_str

    def test_repr_representation(self):
        provider_info = ExternalProviderInfo(
            name=ProviderName("reprprovider"),
            description="Repr provider",
            capabilities=[ExternalProviderCapability.FETCH_LATEST],
        )
        expected_repr = (
            "ExternalProviderInfo(name=ProviderName('reprprovider'), "
            "description='Repr provider', capabilities=[fetch_latest])"
        )
        assert repr(provider_info) == expected_repr

    def test_equality(self):
        provider_info1 = ExternalProviderInfo(
            name=ProviderName("testprovider"),
            description="A test provider",
            capabilities=[ExternalProviderCapability.FETCH_LATEST],
        )
        provider_info2 = ExternalProviderInfo(
            name=ProviderName("testprovider"),
            description="A test provider",
            capabilities=[ExternalProviderCapability.FETCH_LATEST],
        )
        provider_info3 = ExternalProviderInfo(
            name=ProviderName("otherprovider"),
            description="Another provider",
            capabilities=[ExternalProviderCapability.FETCH_BY_USER],
        )

        assert provider_info1 == provider_info2
        assert provider_info1 != provider_info3

    def test_immutability(self):
        provider_info = ExternalProviderInfo(
            name=ProviderName("immutableprovider"),
            description="Immutable provider",
            capabilities=[ExternalProviderCapability.FETCH_LATEST],
        )

        with pytest.raises(AttributeError):
            provider_info.name = ProviderName("newname")

        with pytest.raises(AttributeError):
            provider_info.description = "New description"

        provider_info.capabilities.append(ExternalProviderCapability.FETCH_BY_USER)
        assert len(provider_info.capabilities) == 1
        assert ExternalProviderCapability.FETCH_BY_USER not in provider_info.capabilities

    def test_creation_with_empty_capabilities_should_raise_error(self):
        with pytest.raises(CannotCreateExternalProviderInfoWithEmptyCapabilitiesException):
            ExternalProviderInfo(
                name=ProviderName("emptycapabilities"),
                description="Provider with no capabilities",
                capabilities=[],
            )

    def test_creation_with_invalid_capabilities_should_raise_error(self):
        with pytest.raises(CannotCreateExternalProviderInfoWithInvalidCapabilitiesException):
            ExternalProviderInfo(
                name=ProviderName("invalidcapabilities"),
                description="Provider with invalid capabilities",
                capabilities=["invalid_capability"],
            )

    def test_creation_without_description_should_work(self):
        provider_info = ExternalProviderInfo(
            name=ProviderName("nodescription"),
            capabilities=[ExternalProviderCapability.FETCH_LATEST],
        )

        assert provider_info.name == ProviderName("nodescription")
        assert provider_info.description is None
        assert ExternalProviderCapability.FETCH_LATEST in provider_info.capabilities

    def test_creation_with_none_description_should_work(self):
        provider_info = ExternalProviderInfo(
            name=ProviderName("nonedescription"),
            description=None,
            capabilities=[ExternalProviderCapability.FETCH_LATEST],
        )

        assert provider_info.name == ProviderName("nonedescription")
        assert provider_info.description is None
        assert ExternalProviderCapability.FETCH_LATEST in provider_info.capabilities

    def test_creation_with_none_capabilities_should_raise_error(self):
        with pytest.raises(CannotCreateExternalProviderInfoWithEmptyCapabilitiesException):
            ExternalProviderInfo(
                name=ProviderName("nonecapabilities"),
                description="Provider with None capabilities",
                capabilities=None,
            )

    def test_creation_with_non_list_capabilities_should_raise_error(self):
        with pytest.raises(CannotCreateExternalProviderInfoWithInvalidCapabilitiesException):
            ExternalProviderInfo(
                name=ProviderName("nonlistcapabilities"),
                description="Provider with non-list capabilities",
                capabilities=ExternalProviderCapability.FETCH_LATEST,
            )

    def test_can_evaluate_capability_presence(self):
        provider_info = ExternalProviderInfo(
            name=ProviderName("capabilitytest"),
            description="Testing capability presence",
            capabilities=[
                ExternalProviderCapability.FETCH_LATEST,
                ExternalProviderCapability.FETCH_BY_USER,
            ],
        )

        assert provider_info.has_capability(ExternalProviderCapability.FETCH_LATEST) is True
        assert provider_info.has_capability(ExternalProviderCapability.FETCH_BY_USER) is True
        assert provider_info.has_capability(ExternalProviderCapability.FETCH_BY_TAGS) is False
        assert provider_info.has_capability(ExternalProviderCapability.UPLOAD) is False

    def test_can_be_serialized(self):
        provider_info = ExternalProviderInfo(
            name=ProviderName("serializeprovider"),
            description="Testing serialization",
            capabilities=[ExternalProviderCapability.FETCH_LATEST],
        )
        serialized = provider_info.to_dict()
        assert serialized == {
            "name": "serializeprovider",
            "description": "Testing serialization",
            "capabilities": ["fetch_latest"],
        }

    def test_can_be_deserialized(self):
        data = {
            "name": "deserializeprovider",
            "description": "Testing deserialization",
            "capabilities": ["fetch_latest"],
        }
        provider_info = ExternalProviderInfo.from_dict(data)
        assert provider_info.name == ProviderName("deserializeprovider")
        assert provider_info.description == "Testing deserialization"
        assert ExternalProviderCapability.FETCH_LATEST in provider_info.capabilities
        assert len(provider_info.capabilities) == 1
