"""
GaleriaFora: A microservice for integrating third-party galleries into the MiraVeja ecosystem.

This package provides a pluggable provider pattern for connecting external gallery sources
(DeviantArt, CivitAI, Flickr, Pixiv, etc.) and normalizing their behavior for use within MiraVeja.

Key components:
- configuration: Provider discovery and configuration management
- domain: Core domain models and IExternalProvider interface
- application: Use cases and orchestration logic
- infrastructure: External service clients and storage backends
- api: REST endpoints for MiraVeja integration
"""

from galeriafora.domain import (
    AiMetadata,
    ContentMetadata,
    ContentType,
    ExternalMedia,
    ExternalProviderCapability,
    ExternalProviderInfo,
    MatureRating,
    Page,
    ProviderName,
)

__version__ = "0.1.0"
__author__ = "Jomar Júnior de Souza Pereira"
__email__ = "jomarjunior@poli.ufrj.br"

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    # Domain models
    "ProviderName",
    "Page",
    "MatureRating",
    "ContentType",
    "ContentMetadata",
    "AiMetadata",
    "ExternalProviderCapability",
    "ExternalProviderInfo",
    "ExternalMedia",
]
