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
<<<<<<< HEAD

## Frontend & UI Architecture
**Context:** Need a scalable, maintainable, and responsive frontend interface that easily connects to backend views without code duplication.
**Alternatives considered:** 1. Writing plain HTML/CSS from scratch (Too time-consuming, prone to responsiveness issues).
2. Using a heavy JavaScript framework like React (Overkill for the project scope, breaks Django's built-in rendering flow).
**Decision:** * **Template Design & Reuse:** Utilized Django's template inheritance system. Created `base.html` to house the global navigation and HTML boilerplate.
* **UI Structure:** Integrated Bootstrap 5 via CDN to guarantee mobile responsiveness and accessibility.
* **Integration Decisions:** Used Django template tags (`{% extends %}` and `{% block content %}`) to inject child templates (like `home.html`) into the master layout.
**Code Reference:** `templates/base.html` and `templates/home.html`.
=======
>>>>>>> e37d8cd8377256d29ad006098d90c4d3a55a173c
