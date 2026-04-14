# ADR 0001: System Architecture & Design Philosophies

**Status:** Accepted
**Date:** 2026-04-11
**Lead:** Joshua (Architecture & Setup Lead)

## Decisions
- **Custom User Model:** Implemented `AbstractUser` early to allow for future role-based permissions (LO1).
- **Modular App Division:** Separated `fauna` (data) from `observations` (user logic) to ensure **Loose Coupling**.
- **Template Inheritance:** Centralized UI in `base.html` using Django's template engine to follow the **DRY (Don't Repeat Yourself)** philosophy.

## Member 3 Decisions (Views, Forms & Query Logic Lead)
- **CBVs over FBVs:** 
  - **Context:** We need standard CRUD operations for Observations.
  - **Alternatives:** Function-Based Views with manual `request.method == 'POST'` logic.
  - **Decision:** Used Class-Based Views (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`) as they significantly reduce boilerplate code and follow the DRY principle natively. 
  - **Code Reference:** `echo_nt/observations/views.py:8-46`
- **Form Handling Approach:**
  - **Context:** Collecting user input for creating observations.
  - **Alternatives:** Standard HTML forms or Django `forms.Form`.
  - **Decision:** Utilized `ModelForm` to strictly map input to `Observation` models, saving time on validation. Overrode the `form_valid` method to securely attach the logged-in user without exposing the field on the form.
  - **Code Reference:** `echo_nt/observations/forms.py:4-11` and `echo_nt/observations/views.py:31-33`
- **Query Optimization Decisions:**
  - **Context:** Solving the N+1 query problem associated with rendering `ForeignKey` fields (user, species) in list views.
  - **Alternatives:** Default QuerySet evaluation which runs a query per observation.
  - **Decision:** Implemented `select_related('user', 'species')` within `get_queryset()` of list and detail views mapped over the `Observation` model. This forces SQL JOINs and gathers data efficiently in a single query.
  - **Code Reference:** `echo_nt/observations/views.py:13` and `echo_nt/observations/views.py:22`

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
