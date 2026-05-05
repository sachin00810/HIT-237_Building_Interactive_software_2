# ADR 0003: Centralize Observation Access Rules and Query Boundaries

**Status:** Accepted  
**Date:** 2026-04-15  
**Decision Makers:** Backend logic lead and architecture lead

## Context

EchoNT exposes observation records through several class-based views: list, detail, create, update, and delete. These views need to solve two connected problems at the same time:

- load related `user`, `species`, and habitat data efficiently
- enforce that only the original author can edit or delete an observation

If these concerns are handled separately inside each CBV, the code quickly becomes repetitive and fragile. The list view risks N+1 database behavior, while update and delete views risk inconsistent permission checks if each class reimplements its own authorization logic.

This problem is especially important in the assignment context because the rubric rewards:

- sophisticated class-based view reuse
- object-oriented decomposition
- optimized queryset design
- explicit architectural documentation

The project therefore needed a design that keeps view classes thin while still making data access and authorization behavior explicit and reusable.

## Alternatives Considered

### 1. Implement permission checks and eager loading directly inside each CBV

**Pros**
- Very easy to start with.
- No additional abstractions for small projects.

**Cons**
- Repeats `select_related()` and permission logic across multiple views.
- Makes it easy for one view to miss a security rule or a performance optimization.
- Produces bulky CBVs that are harder to explain in assessment.

### 2. Use function-based views with decorators and manual queryset assembly

**Pros**
- Full control over request flow.
- Straightforward for developers who prefer procedural logic.

**Cons**
- Reintroduces repetitive CRUD code already handled well by Django generic views.
- Works against the project's existing CBV direction.
- Provides a weaker demonstration of OO inheritance and reusable view composition.

### 3. Centralize data access in a queryset mixin and access control in an authorization mixin

**Pros**
- Separates performance concerns from page-specific behavior.
- Reuses the same eager-loading strategy across list, detail, update, and delete views.
- Reuses the same ownership rule across mutating views.
- Strongly demonstrates Django-native OO composition through mixins.

**Cons**
- Adds an abstraction layer that newcomers must trace.
- Requires discipline so future views actually reuse the mixins.

## Decision

The project adopts a mixin-based CBV design:

- `ObservationQuerysetMixin` owns the optimized base queryset
- `AuthorRequiredMixin` owns the "only the author may mutate this record" rule
- concrete CBVs layer request-specific behavior on top of those reusable building blocks

This follows Django philosophy well because it extends generic views instead of replacing them. It also matches OO best practice by separating:

- collection access behavior
- authorization behavior
- page-specific presentation behavior

`ObservationQuerysetMixin` applies `select_related("user", "species")` for the single-valued foreign keys and `prefetch_related("species__habitats")` for the many-to-many habitat relationship. This creates a clear query boundary: each observation page begins from an eager-loaded queryset rather than relying on lazy template access.

`AuthorRequiredMixin` uses `UserPassesTestMixin` and `LoginRequiredMixin` so the authorization rule is expressed once and inherited by both update and delete flows. This is preferable to repeating the same `request.user == object.user` logic in multiple classes.

Overall, the mixin approach was chosen because it best satisfies the rubric's emphasis on CBVs, OO reuse, and advanced QuerySet practice while keeping future extension points clear.

## Code Reference

- `echo_nt/observations/views.py:18-27`
- `echo_nt/observations/views.py:30-40`
- `echo_nt/observations/views.py:43-124`

## Consequences

### Positive consequences

- The list and detail pages inherit a consistent eager-loading policy.
- Update and delete behavior now share a single ownership rule.
- The architecture is easier to explain in ADRs, code review, and demonstration videos.
- Future observation views can reuse the same mixins rather than re-implementing core rules.

### Negative consequences and trade-offs

- New contributors must understand mixin order and method resolution.
- If future views need materially different query behavior, the shared mixin may need to be extended or split.

### Follow-up actions

- Add tests that verify unauthorized users cannot edit or delete another user's observation.
- If observation analytics expand, move aggregate reporting logic into a dedicated `ObservationQuerySet`.
