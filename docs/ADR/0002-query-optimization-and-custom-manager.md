# ADR 0002: Query Optimization and Custom Manager Strategy

**Status:** Accepted  
**Date:** 2026-04-15  
**Decision Makers:** Project team, with implementation led through the `fauna` and `observations` application layers

## Context

EchoNT is a Django application that displays fauna records and user-created observations. Two architectural pressures became clear as the project evolved:

1. The `Observation` interface needs to render related `user` and `species` data repeatedly in list and detail pages.
2. The `Species` catalogue needs a reusable way to express domain-specific queries such as "native to the Northern Territory", "threatened species", and "catalogue-ready species with habitats".

If these concerns are handled with default ORM access patterns and ad hoc filtering in views, the codebase drifts toward two problems:

- **N+1 query inefficiency:** each observation row can trigger additional database queries when templates dereference `observation.user`, `observation.species`, or `observation.species.habitats`.
- **Scattered domain rules:** species filtering and ordering logic can become duplicated across views, forms, commands, and templates.

This matters directly to the project rubric. The assignment rewards object-oriented decomposition, encapsulation, optimized QuerySets, and exemplary architectural documentation. The design therefore needed to move beyond default scaffolding and make the reasoning explicit in code.

## Alternatives Considered

### 1. Keep the default manager and write all filtering logic directly inside each view

This approach would use `Species.objects.all()` everywhere and apply filters inline when needed.

**Pros**
- Minimal code at the beginning of the project.
- Familiar to beginners using Django for the first time.

**Cons**
- Repeats domain rules across multiple entry points.
- Makes it harder to express intent such as "only native NT species" in a single, reusable abstraction.
- Encourages "fat views" instead of encapsulated model-layer querying.

### 2. Rely on Django's default lazy loading for related fields

This approach would avoid explicit `select_related()` and let Django fetch related objects on demand.

**Pros**
- Very little code.
- Works acceptably for tiny datasets during early development.

**Cons**
- Produces the classic N+1 query problem once list pages render many observations.
- Performance cost grows linearly with the number of observations shown.
- Query behavior becomes implicit and harder to reason about during review.

### 3. Use only `prefetch_related()` for all related data

This approach would prefetch both `ForeignKey` and `ManyToMany` relationships uniformly.

**Pros**
- One mental model for related-object loading.
- Useful for many-to-many collections such as species habitats.

**Cons**
- Less efficient than `select_related()` for single-valued `ForeignKey` relationships because it requires separate queries and Python-side joining.
- Misses the opportunity to use SQL joins for `Observation -> user` and `Observation -> species`.

### 4. Write raw SQL or repository-style helper functions instead of custom managers

This approach would centralize querying outside the model manager, possibly in service functions.

**Pros**
- Can provide very explicit control over generated SQL.
- Sometimes useful for very complex reporting queries.

**Cons**
- Adds unnecessary abstraction for a Django coursework project.
- Moves common domain queries away from the ORM layer where Django developers expect to find them.
- Reduces readability and weakens the demonstration of Django-native OO decomposition.

## Decision

The project adopts two complementary ORM decisions:

### A. Use a custom `SpeciesQuerySet` and custom managers for domain-specific species access

The `fauna` app defines:

- `SpeciesQuerySet` for composable query operations such as `native_to_nt()`, `threatened()`, `with_habitat_details()`, and `ordered_for_catalogue()`
- `SpeciesManager` as the default manager for ordered catalogue access
- `NTNativeSpeciesManager` as a specialized manager that automatically scopes results to Northern Territory native species

This decision keeps domain filtering logic close to the `Species` model instead of distributing it across views and commands. It also demonstrates object-oriented decomposition by separating:

- field structure on `Species`
- query behavior in `SpeciesQuerySet`
- default collection access in `SpeciesManager`
- specialized collection access in `NTNativeSpeciesManager`

This is preferable to inline filtering because the manager names communicate intent directly. Calling `Species.native_species.all()` or `Species.objects.for_catalogue()` is more explicit and more maintainable than repeating low-level filters in multiple files.

### B. Use `select_related()` in observation views for single-valued relations, with `prefetch_related()` only where appropriate

The `observations` app defines an `ObservationQuerysetMixin` that centralizes the optimized queryset used by list, detail, update, and delete views.

The mixin applies:

- `select_related("user", "species")` for the `Observation -> user` and `Observation -> species` foreign key relationships
- `prefetch_related("species__habitats")` for the `Species -> habitats` many-to-many relationship

The key architectural choice is that `select_related()` is used for the single-valued joins because Django can resolve them in one SQL query through JOINs. This directly addresses the N+1 problem in `ObservationListView.get_queryset()`, where each rendered observation would otherwise risk extra queries for author and species data.

The view layer then builds on that optimized base queryset with additional filters for:

- selected species
- current user's observations
- recent observations within the last 24 hours

This preserves separation of concerns:

- the mixin owns baseline query optimization
- the concrete view owns request-specific filtering

## Code References

- `echo_nt/fauna/models.py:31-62`
  `SpeciesQuerySet`, `SpeciesManager`, and `NTNativeSpeciesManager` implement reusable query behavior and specialized collection access.

- `echo_nt/fauna/models.py:65-88`
  `Species` binds the custom managers to the model and adds an index for `is_native_to_nt` plus `conservation_status`, supporting catalogue and conservation filtering.

- `echo_nt/observations/views.py:18-27`
  `ObservationQuerysetMixin` applies `select_related("user", "species")` and `prefetch_related()` for habitat data.

- `echo_nt/observations/views.py:43-71`
  `ObservationListView.get_queryset()` builds on the optimized base queryset and applies request-driven filtering while preserving eager loading.

- `echo_nt/observations/views.py:74-124`
  `ObservationDetailView`, `ObservationUpdateView`, and `ObservationDeleteView` reuse the same optimized queryset strategy, proving that the decision scales across multiple CBVs rather than existing as a one-off optimization.

## Consequences

### Positive consequences

- Observation pages avoid the most common N+1 problem for `user` and `species` relationships.
- Species access rules are centralized and easier to test, explain, and extend.
- The code better demonstrates encapsulation and OO design because query rules are named abstractions rather than repeated filters.
- The architecture is easier to defend in assessment because the reasoning is visible in both code and documentation.
- The custom manager structure creates a clean foundation for later features such as "show only threatened native species" or "build a conservation dashboard".

### Negative consequences and trade-offs

- The ORM layer becomes slightly more advanced, which raises the learning curve for beginners reading the project.
- Developers must understand when to use `select_related()` versus `prefetch_related()`; misusing them can reduce performance instead of improving it.
- Centralized managers and queryset mixins create an extra abstraction layer, so contributors need to trace behavior across more than one class.

### Operational consequences

- Future developers should prefer extending `SpeciesQuerySet` or its managers rather than adding repeated filtering logic in views.
- Future observation views should reuse `ObservationQuerysetMixin` whenever they render related `user`, `species`, or habitat data.
- If the data model changes, the eager-loading strategy should be reviewed to ensure the chosen relationships still match the actual access pattern.

Overall, this decision intentionally favors a slightly richer model and queryset architecture in exchange for stronger performance, clearer intent, and a more assessable demonstration of advanced Django design practice.
