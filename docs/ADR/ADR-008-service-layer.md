# ADR-008: Use Service Layer for Business Logic

## Status
Accepted

## Context
The project had business logic inside views, especially when creating observations. This made the views responsible for too many things, including handling forms, saving objects, assigning the author, and returning responses.

## Decision
We decided to create a service layer using `observations/services.py`.

The service layer contains functions such as:
- `create_observation()`
- `get_user_observations()`
- `verify_observation()`
- `delete_observation()`

Views should only handle request and response. Services should handle business logic.

## Consequences
This improves separation of concerns, maintainability, and testability. It also makes the code easier to explain during the viva because the business logic is in one clear place.