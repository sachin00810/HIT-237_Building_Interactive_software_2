# ADR 0001: System Architecture & Design Philosophies

**Status:** Accepted
**Date:** 2026-04-11
**Lead:** Joshua (Architecture & Setup Lead)

## Decisions
- **Custom User Model:** Implemented `AbstractUser` early to allow for future role-based permissions (LO1).
- **Modular App Division:** Separated `fauna` (data) from `observations` (user logic) to ensure **Loose Coupling**.
- **Template Inheritance:** Centralized UI in `base.html` using Django's template engine to follow the **DRY (Don't Repeat Yourself)** philosophy.

## Rationale
This structure ensures that the "Bio-Validation Engine" can be developed independently of the Web UI, adhering to **Sophisticated OO Decomposition (LO3)**.
