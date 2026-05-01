# ADR 0004: Custom User Model vs Profile Model

**Status:** Accepted  
**Date:** 2026-05-01  
**Context:**  
To support different user roles (viewers, rangers, and researchers) within the EchoNT application, we needed a way to store and retrieve a user's role efficiently. The main alternatives in Django are extending the built-in `AbstractUser` to create a Custom User Model, or creating a separate one-to-one `Profile` model linked to the default `User`.

**Alternatives:**
1. **Custom User Model (Extending `AbstractUser`):** Stores additional fields directly on the user table. Recommended by Django documentation for new projects.
2. **Profile Model (One-to-One):** Creates a separate table linked to `User`. Better for retrofitting existing projects where swapping the User model is difficult.

**Decision:**  
We decided to use a **Custom User Model** (`CustomUser` extending `AbstractUser`) and added a `role` field directly to it.

**Code Reference:**  
- `echo_nt/users/models.py:4` - Definition of `CustomUser` and `ROLE_CHOICES`.

**Consequences:**  
- **Pros:** Simpler database schema (avoids extra JOINs for profile data), easier to access in templates (e.g., `user.role`), and aligns with Django best practices.
- **Cons:** Any future field additions to the user model require schema migrations on the core authentication table, which can be sensitive.
