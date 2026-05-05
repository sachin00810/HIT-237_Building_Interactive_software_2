# EchoNT Object-Oriented Class Diagram

This diagram reflects the actual implementation of the EchoNT Biodiversity Monitoring system. It highlights **Inheritance** (CustomUser extends AbstractUser), **Aggregation** (Observation links User and Species), **Association** (Species ↔ Habitat M2M), and the **role-based auth model** introduced in Assessment 4.

```mermaid
classDiagram
    direction LR

    %% ── Auth App (users) ────────────────────────────────────────────
    class AbstractUser {
        <<Django Core>>
        +int id
        +String username
        +String email
        +String password
        +bool is_active
        +bool is_staff
        +DateTime date_joined
    }

    class CustomUser {
        <<App: users>>
        +String role
        +ROLE_CHOICES viewer|ranger|researcher
        +__str__() String
    }

    AbstractUser <|-- CustomUser : extends

    %% ── Fauna App ───────────────────────────────────────────────────
    class Habitat {
        <<App: fauna>>
        +int id
        +String name
        +Text description
        +__str__() String
    }

    class Species {
        <<App: fauna>>
        +int id
        +String name
        +String scientific_name
        +String conservation_status
        +Text summary
        +bool is_native_to_nt
        +display_name() String
        +is_threatened() bool
        +__str__() String
    }

    Species "*" --> "*" Habitat : habitats (M2M)

    %% ── Observations App ────────────────────────────────────────────
    class Observation {
        <<App: observations>>
        +int id
        +Text notes
        +DateTime date_spotted
        +bool is_verified
        +DateTime created_at
        +DateTime updated_at
        +notes_excerpt() String
        +is_recent_sighting() bool
        +__str__() String
    }

    CustomUser "1" --> "*" Observation : user (FK, CASCADE)
    Species "1" --> "*" Observation : species (FK, PROTECT)

    %% ── Access Control (no separate model — enforced via mixins) ────
    class AuthorRequiredMixin {
        <<Mixin: observations/views.py>>
        +test_func() bool
        +handle_no_permission()
    }

    class RangerRequiredMixin {
        <<Mixin: observations/views.py>>
        +test_func() bool
        +handle_no_permission()
    }

    AuthorRequiredMixin ..> Observation : checks user_id == request.user.id
    RangerRequiredMixin ..> CustomUser : checks role == ranger
```

## Auth Model Notes

| Role | Can create observations | Can edit/delete own | Can verify any |
|------|------------------------|---------------------|----------------|
| viewer | Yes (login required) | Yes | No |
| researcher | Yes (login required) | Yes | No |
| ranger | Yes (login required) | Yes | Yes |

- Role is stored directly on `CustomUser` (field: `role`) rather than via Django Groups — see [ADR 0004](../docs/0004-custom-user-model-vs-profile.md).
- Object-level permissions are enforced by `AuthorRequiredMixin` and `RangerRequiredMixin` — see [ADR 0005](../docs/0005-mixin-vs-decorator-access-control.md) and [ADR 0006](../docs/0006-object-level-permissions.md).
