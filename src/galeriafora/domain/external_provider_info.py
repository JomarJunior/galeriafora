from typing import List, Optional

from galeriafora.domain.exceptions import (
    CannotCreateExternalProviderInfoWithEmptyCapabilitiesException,
    CannotCreateExternalProviderInfoWithEmptyNameException,
    CannotCreateExternalProviderInfoWithInvalidCapabilitiesException,
)
from galeriafora.domain.external_provider_capability import ExternalProviderCapability
from galeriafora.domain.provider_name import ProviderName


class ExternalProviderInfo:
    def __init__(
        self,
        name: ProviderName,
        capabilities: List[ExternalProviderCapability],
        description: Optional[str] = None,
    ):
        if not name or not name._name.strip():
            raise CannotCreateExternalProviderInfoWithEmptyNameException()
        if not capabilities:
            raise CannotCreateExternalProviderInfoWithEmptyCapabilitiesException()
        if not all(isinstance(cap, ExternalProviderCapability) for cap in capabilities):
            raise CannotCreateExternalProviderInfoWithInvalidCapabilitiesException()

        self._name = name
        self._description = description
        self._capabilities = capabilities

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def capabilities(self):
        return list(self._capabilities)

    @classmethod
    def from_dict(cls, data: dict) -> "ExternalProviderInfo":
        name = ProviderName(data["name"])
        description = data.get("description")
        capabilities = [ExternalProviderCapability(cap) for cap in data["capabilities"]]
        return cls(name=name, description=description, capabilities=capabilities)

    def has_capability(self, capability: ExternalProviderCapability) -> bool:
        return capability in self._capabilities

    def __str__(self):
        capabilities_str = ", ".join(cap.value for cap in self.capabilities)
        return (
            f"ExternalProviderInfo(name={self.name}, "
            f"description='{self.description}', capabilities=[{capabilities_str}])"
        )

    def __repr__(self):
        capabilities_repr = ", ".join(repr(cap) for cap in self.capabilities)
        return (
            f"ExternalProviderInfo(name={repr(self.name)}, "
            f"description='{self.description}', capabilities=[{capabilities_repr}])"
        )

    def __eq__(self, other):
        if not isinstance(other, ExternalProviderInfo):
            return NotImplemented
        return (
            self.name == other.name
            and self.description == other.description
            and set(self.capabilities) == set(other.capabilities)
        )

    def to_dict(self) -> dict:
        return {
            "name": str(self.name),
            "description": self.description,
            "capabilities": [cap.value for cap in self.capabilities],
        }
