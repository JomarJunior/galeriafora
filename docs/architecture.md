# 🎨 GaleriaFora - Architecture Overview

This document provides an architectural overview of the **GaleriaFora** project, detailing its core components, design principles, and integration with the broader **🖼️ MiraVeja** ecosystem. It serves as a guide for developers and contributors to understand the structure and rationale behind the implementation of GaleriaFora.

---

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Design Principles](#design-principles)
3. [System Overview](#system-overview)
   - [High-Level Diagram](#high-level-diagram)
   - [Core Modules](#core-modules)
4. [Domain Layer](#domain-layer)
5. [Application Layer](#application-layer)
6. [External Providers](#external-providers)
7. [Integration with MiraVeja](#integration-with-miraveja)
8. [Plugin System](#plugin-system)
9. [Data Models](#data-models)
10. [Dependency Management & CI/CD](#dependency-management--cicd)
11. [Testing Strategy](#testing-strategy)
12. [Future Considerations](#future-considerations)

---

## 1. Introduction

GaleriaFora is designed to serve as a robust media management solution within the **🖼️ MiraVeja** ecosystem. Its mission is to streamline the integration of various third-party gallery providers, enhancing the overall user experience by providing seamless access to diverse media sources.

The project enhances **🖼️ MiraVeja** by offering a unified interface for managing and displaying media from multiple external galleries, thereby simplifying the process for developers and contributors. Target users include developers looking to extend functionality, contributors aiming to improve the platform, and end-users who benefit from a richer media experience.

Additionally, GaleriaFora addresses the challenges of integrating third-party galleries by implementing a flexible plugin system, allowing for easy addition and management of new providers without disrupting the core architecture.

---

## 2. Design Principles

GaleriaFora is built on a foundation of established software engineering principles designed to ensure maintainability, scalability, and extensibility:

### Hexagonal Architecture (Ports & Adapters)

The application is organized into concentric layers: Domain (business logic), Application (use cases), and Infrastructure (external integrations). This isolation allows the core business logic to remain independent of framework specifics and external providers, making testing and evolution straightforward.

### Domain-Driven Design (DDD)

Business rules and entities live at the core, with clear bounded contexts separating provider integrations from media management. Ubiquitous language is maintained across code, documentation, and team communication to reduce friction between technical and domain experts.

### Test-Driven Development (TDD)

Testing is prioritized throughout development. Unit tests cover domain and application logic, contract tests validate provider adapters, and integration tests ensure async workflows function correctly. High coverage is enforced in CI/CD pipelines.

### Extensibility & Maintainability

The plugin system allows new providers to be added without modifying core code. Clear contracts (interfaces/ports) between layers enable straightforward refactoring and updates. Dependency injection facilitates loose coupling and testability.

### Async-First & Performance

Async/await patterns are employed for I/O-bound operations (API calls, database queries, file transfers). Non-blocking workflows prevent bottlenecks when handling multiple providers and large media volumes.

### Plugin-First Mindset

GaleriaFora treats even built-in providers as plugins, standardizing the extensibility model. This ensures that internal and third-party providers follow the same discovery and lifecycle conventions, reducing complexity and friction.

---

## 3. System Overview

### Architecture Layers

GaleriaFora follows a layered architecture pattern:

```text
┌─────────────────────────────────────────────────┐
│         MiraVeja (Consumer Application)         │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│      Application Layer (Use Cases)              │
│  - Media orchestration                          │
│  - Provider coordination                        │
│  - Caching & pagination                         │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│      Domain Layer (Business Logic)              │
│  - Entities & value objects                     │
│  - Port definitions (interfaces)                │
│  - Business rules                               │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│   Infrastructure Layer (External Integration)   │
│  - Provider adapters                            │
│  - API clients                                  │
│  - Cache connectors                             │
│  - Third-party gallery APIs                     │
└─────────────────────────────────────────────────┘
```

### Core Components

- **Domain**: Defines core entities (e.g., `ExternalMedia`), value objects, and the `IExternalProvider` interface that all providers must implement.
- **Application**: Orchestrates provider actions, handles caching, pagination, and async operations
- **Infrastructure**: Concrete provider implementations (adapters), client factories, and external service integrations
- **Plugin System**: Runtime provider discovery via entry points, enabling extensibility without core modifications

### High-Level Diagram

```text
┌──────────────────────────────────────────────────────────────────┐
│                     MiraVeja UI / API Layer                      │
└────────────────────────────┬─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│         GaleriaFora Application Layer (Orchestration)            │
│  - MediaFetcher, MediaUploader, ProviderCoordinator              │
└────────────────────────────┬─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│         GaleriaFora Domain Layer (Business Rules)                │
│  - IExternalProvider (Port / Interface)                          │
│  - ExternalMedia, ExternalProviderInfo (Value Objects)           │
└────────────────────────────┬─────────────────────────────────────┘
                             │
         ┌───────────────────┼──────────────────────┐
         │                   │                      │
    ┌────▼─────┐       ┌─────▼───────┐        ┌─────▼────┐
    │ Provider │       │ Provider    │        │ Provider │
    │ Adapter  │       │ Adapter     │        │ Adapter  │
    │ (Flickr) │       │ (DeviantArt)│        │ (Custom) │
    └────┬─────┘       └────┬────────┘        └─────┬────┘
         │                  │                       │
    ┌────▼────┐       ┌─────▼───────┐          ┌────▼────┐
    │ Flickr  │       │ DeviantArt  │          │ External│
    │ API     │       │ API         │          │ Service │
    └─────────┘       └─────────────┘          └─────────┘
```

### Core Modules

**Expected content for each module:**

- **Domain**: Entities, Value Objects, Ports (interfaces)
- **Application**: Use cases, service orchestration, business logic
- **Infrastructure**: Provider clients, database connectors, caching, storage
- **Presentation / API**: Optional if used for internal services

---

## 4. Domain Layer

The Domain Layer encapsulates the core business logic and rules of GaleriaFora. It defines the main entities, value objects, and interfaces that represent the core concepts of media management and provider interactions.

### Main Concepts

#### AiMetadata

The `AiMetadata` value object captures metadata about the AI generation status of media items, including whether they are AI-generated and any relevant tags or attributes.

```json
{
    "is_ai_generated": "boolean",
    // ... additional fields as needed
}
```

#### ExternalMedia

The `ExternalMedia` value object represents the canonical media item fetched from an external provider.

```json
{
    "url": "string",
    "title": "string",
    "description": "string",
    "tags": ["string"],
    "rating": "Rating",
    "ai_metadata": "AiMetadata",
    "provider": "ExternalProviderInfo"
}
```

#### Rating

The `Rating` enumeration defines the content rating of media items, such as `PG`, `PG-13`, `R`, etc., which can be used for filtering and display purposes.

```python
from enum import Enum

class Rating(str, Enum):
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    X = "X"
    XXX = "XXX"

    def __str__(self):
        return self.value
```

#### ExternalProviderInfo

The `ExternalProviderInfo` value object contains metadata sufficient to identify the provider and its capabilities.

```json
{
    "name": "ExternalProviderName",
    "description": "string",
    "capabilities": ["ExternalProviderCapability"]
}
```

#### Page

The `Page` value object is a generic pagination wrapper used for fetching media in batches.

```json
{
    "items": ["Generic"],
    "next_cursor": "string",
    "has_more": "boolean"
}
```

#### ProviderName

The `ProviderName` is a value object that represents the unique identifier for a provider, used for normalization.

```json
{
    "value": "string"
}
```

Normalization rules for provider names ensure that different variations (e.g., "DeviantArt", "deviant-art", "DeViAnArT") are standardized to a consistent format (e.g., "deviantart") for internal use. Display-friendly names should be handled by the UI layer, allowing for flexibility in presentation while maintaining stable identifiers in the domain logic.

Regex pattern for normalization allows only lowercase letters and numbers. Any non-alphanumeric characters are removed, and uppercase letters are converted to lowercase. This ensures that provider names are consistent and can be reliably used as identifiers across the system.

Pattern: `^[a-z0-9]+$`

#### ProviderCapability

The `ProviderCapability` is an enumeration that defines the specific actions a provider can perform, such as `fetch_latest`, `fetch_by_user`, `fetch_by_tags`, and `upload`.

```python
from enum import Enum

class ProviderCapability(Enum):
    FETCH_LATEST = "fetch_latest"
    FETCH_BY_USER = "fetch_by_user"
    FETCH_BY_TAGS = "fetch_by_tags"
    UPLOAD = "upload"

    def __str__(self):
        return self.value
```

### IExternalProvider Interface

The `IExternalProvider` interface defines the contract that all provider implementations must adhere to. It includes methods for fetching media based on various criteria and uploading media when supported.

```python
from abc import ABC, abstractmethod

class IExternalProvider(ABC):
    @property
    @abstractmethod
    def info(self) -> ExternalProviderInfo:
        pass

    @abstractmethod
    async def fetch_latest(self, page: int = 1) -> Page[ExternalMedia]:
        pass

    @abstractmethod
    async def fetch_by_user(self, username: str, page: int = 1) -> Page[ExternalMedia]:
        pass

    @abstractmethod
    async def fetch_by_tags(self, tags: List[str], page: int = 1) -> Page[ExternalMedia]:
        pass

    @abstractmethod
    async def upload(self, media: ExternalMedia) -> bool:
        pass
```

---

## 5. Application Layer

The Application Layer provides the orchestration logic and use cases that coordinate interactions between the domain layer and infrastructure layer. It is responsible for managing provider actions, caching strategies, pagination handling, and async workflows while maintaining the isolation of the domain layer from external concerns.

### Core Principles

- **Port-Based Design**: The application layer depends exclusively on domain ports (`IExternalProvider`) rather than concrete implementations, ensuring loose coupling and testability.
- **Separation of Concerns**: Business orchestration logic is isolated from technical infrastructure concerns (API clients, databases, caching mechanisms).
- **Async-First**: All provider interactions and I/O operations are non-blocking, enabling concurrent handling of multiple providers and large media volumes.

### Key Services

#### MediaFetcher

Responsible for retrieving media from one or more providers with support for filtering, pagination, and caching.

```python
class MediaFetcher:
    async def fetch_latest(self, provider_name: str, page: int = 1) -> Page[ExternalMedia]:
        # Consult cache; delegate to provider if needed
        pass

    async def fetch_by_user(self, provider_name: str, username: str, page: int = 1) -> Page[ExternalMedia]:
        # Validate capability; fetch and cache
        pass

    async def fetch_by_tags(self, provider_name: str, tags: List[str], page: int = 1) -> Page[ExternalMedia]:
        # Validate capability; fetch and cache
        pass

    async def fetch_from_all_providers(self, capability: ProviderCapability) -> List[ExternalMedia]:
        # Concurrent fetching from multiple providers
        pass
```

#### MediaUploader

Handles uploading media to providers that support the `upload` capability, with retry logic and error handling.

```python
class MediaUploader:
    async def upload(self, provider_name: str, media: ExternalMedia) -> bool:
        # Validate capability; execute upload with retries
        pass

    async def upload_to_multiple(self, media: ExternalMedia, providers: List[str]) -> Dict[str, bool]:
        # Concurrent uploads with fallback and error tracking
        pass
```

#### ProviderCoordinator

Discovers and manages available providers, exposing capability queries and provider metadata.

```python
class ProviderCoordinator:
    def get_provider(self, name: ProviderName) -> IExternalProvider:
        # Retrieve provider instance
        pass

    def list_providers(self) -> List[ExternalProviderInfo]:
        # Return all registered providers
        pass

    def get_providers_by_capability(self, capability: ProviderCapability) -> List[IExternalProvider]:
        # Filter providers by supported capability
        pass
```

### Caching Strategy

Caching layers are applied transparently to reduce redundant API calls:

- **Media Cache**: Stores fetched media results keyed by provider, query parameters, and page number.
- **Provider Metadata Cache**: Caches provider info and capabilities with longer TTLs.
- **Cache Invalidation**: Time-based expiration and manual invalidation on upload operations.

### Pagination & Bulk Operations

- **Cursor-Based Pagination**: The `Page` value object supports both offset and cursor-based pagination for flexibility across different provider APIs.
- **Lazy Loading**: Media is fetched on-demand as pagination cursors advance, preventing memory overhead.
- **Bulk Fetch**: `fetch_from_all_providers` uses `asyncio.gather()` to concurrently request from all providers, with fallback logic for failures.

### Integration Points with MiraVeja

The application layer exposes high-level use cases that MiraVeja consumes:

- **Get Latest Media**: Fetch trending or recent media across all or selected providers.
- **Search by User**: Query media authored by specific users on enabled providers.
- **Search by Tags**: Find media matching given tags across multiple sources.
- **Upload Media**: Push media to providers supporting the `upload` capability.

### Async Workflows & Concurrency

- **Non-Blocking I/O**: All provider API calls and database operations use async patterns to prevent thread blocking.
- **Concurrent Provider Queries**: Multiple providers are queried in parallel using `asyncio.gather()` or `asyncio.TaskGroup()`.
- **Error Resilience**: If one provider fails, others continue; failures are logged and surfaced without blocking the entire operation.
- **Rate Limiting**: Built-in request throttling ensures compliance with provider API limits across concurrent requests.

---

## 6. External Providers

GaleriaFora integrates third-party gallery providers through a well-defined provider adapter pattern, allowing for seamless interaction with various external APIs.

### Provider Adapter Pattern

Each third-party provider is represented by an adapter that implements the `IExternalProvider` interface. This design encapsulates the specific API interactions and abstracts the underlying complexities, enabling a consistent interface for the application layer.

### Client Injection

To facilitate authentication and API interaction, client instances are injected into the provider adapters. This allows for flexible configuration of authentication methods (e.g., API keys, OAuth tokens) and ensures that each provider can manage its own connection settings.

### Example Capabilities

Providers implement several key capabilities, including:

- **fetch_latest**: Retrieves the most recent media items from the provider.
- **fetch_by_user**: Fetches media items associated with a specific user.
- **fetch_by_tags**: Queries media items based on specified tags.
- **upload**: Allows for uploading media items back to the provider.

### Mapping Capabilities to Domain Actions

Each capability directly maps to actions within the domain layer, ensuring that the application layer can orchestrate media operations without needing to know the specifics of each provider's API. This mapping maintains a clean separation of concerns and enhances maintainability.

### Error Handling and Retry Strategy

Robust error handling is implemented within each provider adapter. If an API call fails, the adapter can retry the request based on predefined strategies, such as exponential backoff. This ensures resilience against transient errors and improves the overall reliability of the media fetching and uploading processes.

---

## 7. Integration with MiraVeja

GaleriaFora plays a crucial role in the broader **🖼️ MiraVeja** ecosystem by providing a seamless integration layer for various media sources. This integration is facilitated through well-defined entry points and a structured application layer that exposes functionality to the UI and API layers.

### Application Layer Functionality

The application layer orchestrates interactions between the domain layer and external providers. It exposes high-level use cases that can be consumed by the UI or API layers, allowing developers to fetch, cache, and display media efficiently.

### UI and API Layer Consumption

The UI or API layers interact with the application layer to perform operations such as fetching the latest media, searching by user or tags, and uploading media. This interaction is designed to be straightforward, ensuring that developers can easily integrate GaleriaFora's capabilities into their applications.

### Lifecycle of Media

The lifecycle of media within GaleriaFora follows a clear path:

1. **Fetch**: Media is retrieved from external providers based on user queries or predefined criteria.
2. **Cache**: Fetched media is stored in a caching layer to reduce redundant API calls and improve performance.
3. **Upload**: Users can upload media back to providers that support this capability, with the application layer managing the process.
4. **Display**: Finally, the media is presented to users through the UI, ensuring a rich and engaging experience.

### Event-Driven or Asynchronous Updates

GaleriaFora employs asynchronous patterns to handle media operations, allowing for non-blocking interactions with multiple providers. This design ensures that updates to media are processed efficiently, enabling real-time or near-real-time updates in the UI as new media is fetched or uploaded.

---

## 8. Plugin System

GaleriaFora employs a robust extensibility model that allows for seamless integration of new providers without altering the core architecture. This model is designed to facilitate easy addition, management, and discovery of third-party plugins.

### Entry Points Registration

Providers are registered through a dedicated entry point located in the `galeriafora.providers` module. This module serves as a centralized registry where all available providers can be listed and accessed.

### Adding New Providers

New providers can be added by implementing the `IExternalProvider` interface and registering them in the entry point. This approach ensures that the core codebase remains untouched, promoting maintainability and reducing the risk of introducing bugs.

### Provider Discovery at Runtime

GaleriaFora utilizes a runtime discovery mechanism to identify and load available providers dynamically. This allows the application to adapt to new providers as they are added, ensuring that users can benefit from the latest integrations without requiring application restarts or redeployments.

### Versioning and Compatibility Considerations

To maintain compatibility across different provider versions, GaleriaFora implements a versioning strategy that allows providers to specify their supported versions. This ensures that changes in provider APIs do not disrupt existing functionality and that users can choose to upgrade or downgrade providers as needed.

### Security Considerations for Third-Party Plugins

Security is a paramount concern when integrating third-party plugins. GaleriaFora enforces strict validation and sanitization of inputs from providers to mitigate risks such as injection attacks or data breaches. Additionally, plugins are executed in a controlled environment to limit their access to sensitive application resources.

---

## 10. Dependency Management & CI/CD

### Dependency Management

GaleriaFora uses **Poetry** for robust dependency management and virtual environment isolation:

- **pyproject.toml**: All dependencies are declared with version constraints, separating production and development dependencies.
- **poetry.lock**: Ensures reproducible builds by pinning exact versions across all environments.
- **Version Pinning Strategy**: Production dependencies use caret (`^`) constraints to allow patch updates while preventing breaking changes; development dependencies (pytest, mypy, ruff) use flexible ranges to stay current.
- **Virtual Environment Isolation**: Poetry automatically creates isolated environments, preventing conflicts with system packages.

### CI/CD Pipeline

GaleriaFora employs a GitHub Actions workflow that runs on every push and pull request:

#### Build & Environment Setup

- Checks out code and caches Poetry virtualenv to accelerate subsequent runs
- Installs dependencies via `poetry install` with locked versions

#### Code Quality Checks

- **Linting**: `ruff check` enforces code style and catches common errors
- **Format Verification**: `ruff format --check` ensures consistent formatting
- **Type Checking**: `mypy` validates type annotations across the codebase

### Testing

- **Unit Tests**: `pytest` with coverage reporting on domain and application layers
- **Contract Tests**: Validates provider adapter implementations against the `IExternalProvider` interface
- **Integration Tests**: Verifies async workflows and provider orchestration
- **Coverage Enforcement**: CI fails if coverage drops below configured thresholds (typically 80%+)

### Caching Strategies

- **Poetry Cache**: Caches the dependency resolver output to speed up `poetry install`
- **Virtualenv Cache**: Caches the entire virtual environment using `actions/cache`, reducing installation time from minutes to seconds on subsequent runs

### Artifact Management

- Test reports and coverage summaries are generated and archived for visibility

---

## 11. Testing Strategy

### Unit Tests for Domain & Application Layers

Domain and application layer tests focus on business logic without external dependencies:

- **Domain Tests**: Validate entity creation, value object invariants (e.g., `ProviderName` normalization), and enum behaviors (`Rating`, `ProviderCapability`).
- **Application Service Tests**: Mock `IExternalProvider` implementations to test orchestration logic in `MediaFetcher`, `MediaUploader`, and `ProviderCoordinator` without invoking real APIs.
- **Use Case Tests**: Verify end-to-end workflows (fetch → cache → paginate) with injected mock providers.

### Contract Tests for Providers

Contract tests ensure that each provider adapter conforms to the `IExternalProvider` interface:

- **Interface Compliance**: Verify all required methods exist and accept correct parameters.
- **Response Shape Validation**: Confirm that `Page`, `ExternalMedia`, and `ExternalProviderInfo` objects are constructed with valid data.
- **Capability Mapping**: Validate that declared capabilities in `info()` match implemented methods.
- **Error Handling**: Test retry logic and graceful degradation when APIs fail or rate limits are exceeded.

### Integration Tests for Async Workflows

Integration tests validate concurrent provider interactions and real async behavior:

- **Concurrent Fetching**: Test `fetch_from_all_providers()` with multiple providers running in parallel.
- **Cache Invalidation**: Verify caching behavior across sequential and concurrent requests.
- **Error Resilience**: Confirm that if one provider fails, others continue and results are aggregated correctly.
- **Real Async Patterns**: Use `pytest-asyncio` to run actual async code paths.

### Test Coverage & CI Enforcement

- **Coverage Thresholds**: Enforce minimum 80% coverage on domain and application layers via `pytest-cov`.
- **Exclusions**: Exclude infrastructure adapters from strict coverage to allow for flexibility in provider implementations.
- **CI Gating**: Pull requests fail if coverage drops below configured thresholds, preventing regressions.
- **Coverage Reports**: Generate and publish HTML reports in CI artifacts for visibility.

### Mocking & Dependency Injection Approach

- **Fixture-Based Mocking**: Use `pytest` fixtures to provide mock `IExternalProvider` instances with configurable behavior (e.g., returning specific `Page` objects or raising exceptions).
- **Dependency Injection**: Services receive providers via constructor injection, enabling straightforward test doubles without modifying production code.
- **AsyncMock**: Use `unittest.mock.AsyncMock` for async methods to simulate provider behavior.
- **Factory Patterns**: Test double factories create consistent mock providers with controlled responses, reducing test boilerplate.

---

## 12. Future Considerations

### Adding New Provider Capabilities

As GaleriaFora evolves, new capabilities may emerge (e.g., `fetch_by_collection`, `batch_upload`, `stream_live`). The extension model allows capabilities to be added to the `ProviderCapability` enum without breaking existing providers. New interface methods in `IExternalProvider` can be introduced with default implementations or optional protocols to maintain backward compatibility. Provider implementations adopt new capabilities at their own pace, and the application layer uses capability queries to determine supported actions.

### Scaling to Large Media Volumes

Current pagination handles moderate datasets, but scaling to millions of items requires enhancements. Strategies include implementing distributed caching (Redis/Memcached) for shared environments, adopting cursor-based pagination exclusively to avoid offset inefficiencies, and introducing batch processing with background workers (Celery/RQ) for non-blocking bulk operations. Database indexing on provider names and tags will be critical. Stream-based result processing and lazy evaluation patterns will minimize memory overhead during concurrent multi-provider queries.

### Integration with NFTs or Decentralized Storage

Future versions may support blockchain-based galleries and decentralized storage (IPFS, Arweave). New provider adapters implementing `IExternalProvider` can abstract interactions with Web3 APIs, smart contracts, and decentralized protocols. The domain layer will expand to include blockchain-specific metadata (e.g., wallet addresses, contract IDs, token URIs). Security considerations include safe handling of private keys and contract verification to prevent fraud.

### Migration Paths for New Python and Library Versions

Maintaining compatibility with Python 3.10+ and managing library upgrades requires proactive planning. Regular dependency audits via tools like `dependabot` or `pip-audit` will identify security updates and compatibility issues. Major library migrations (e.g., Pydantic v1 to v2, asyncio framework changes) will be staged in feature branches with comprehensive testing. Deprecation policies will be documented, signaling when legacy Python versions are no longer supported. Documentation will include upgrade guides and breaking change notices.

---

*End of Document*
