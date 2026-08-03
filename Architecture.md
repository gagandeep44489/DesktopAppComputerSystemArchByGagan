# Architecture

The application follows Clean Architecture:

- `domain`: enterprise entities and repository contracts.
- `application`: reserved for orchestration and use-cases as features grow.
- `infrastructure`: API clients, mock adapters, HTTP client, and repository implementations.
- `presentation`: Material UI components, pages, feature hooks, validation, and layouts.
- `app`: composition root, providers, dependency injection, and routing.

UI components never instantiate APIs directly. Components call hooks, hooks use injected repositories, and repositories delegate to API adapters.
