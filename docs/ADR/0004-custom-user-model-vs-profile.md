# ADR 0004: Custom User Model vs Profile Model

**Status:** Accepted  
**Date:** 2026-05-01  
**Author:** Sachin

## Context
To support different user roles (viewers, rangers, and researchers) within the EchoNT application, we needed a way to store and retrieve a user's role efficiently. The main alternatives in Django are extending the built-in `AbstractUser` to create a Custom User Model, or creating a separate one-to-one `Profile` model linked to the default `User`.

## Alternatives Considered

1. **Custom User Model (Extending `AbstractUser`):** Stores additional fields directly on the user table. Recommended by Django documentation for new projects. Requires setting `AUTH_USER_MODEL` before the first migration.
2. **Profile Model (One-to-One):** Creates a separate `UserProfile` table linked to `User` via a `OneToOneField`. Better for retrofitting existing projects where swapping the User model is impractical. Requires joins on every auth-related query.
3. **Django Groups + Permissions:** Use Django's built-in `Group` model (e.g., a "Rangers" group) rather than a custom field. More flexible but adds database overhead and complexity for a simple 3-role model.

## Decision
We decided to use a **Custom User Model** (`CustomUser` extending `AbstractUser`) and added a `role` CharField directly to it.

**Code Reference:**
- `echo_nt/users/models.py:4` — Definition of `CustomUser` and `ROLE_CHOICES`
- `echo_nt/config/settings.py:116` — `AUTH_USER_MODEL = 'users.CustomUser'`

## Consequences

**Pros:**
- Simpler database schema — avoids extra JOINs when checking a user's role in views and templates.
- Direct template access: `{{ user.role }}` without prefetching a related object.
- Aligns with Django's own recommendation: setting a custom user model from day one avoids painful migrations later.

**Cons:**
- Future field additions to the user model require migrations on the core authentication table, which is a sensitive operation in production.
- The `AUTH_USER_MODEL` setting cannot be changed after the first migration without resetting the database.

## Security Implications

**Session-based vs Token-based Authentication:**  
EchoNT uses Django's default **session-based authentication** rather than token/JWT authentication. This decision was made deliberately:

| Consideration | Session (chosen) | Token / JWT |
|---|---|---|
| State | Stateful — session stored server-side | Stateless — token carries all claims |
| CSRF | Django's `CsrfViewMiddleware` provides automatic protection | Must be manually handled |
| Revocation | Instant — delete the session record | Difficult — tokens are valid until expiry |
| Mobile clients | Less suitable (cookie-based) | Better for REST/mobile APIs |
| Complexity | Low — built into Django | Higher — requires token issuance, refresh logic |

Since EchoNT is a **server-rendered Django application** with no mobile client or external API consumers, session-based auth is the correct choice. The CSRF middleware is active in `settings.py:42`, providing automatic protection for all POST endpoints including the observation verify view.

**Migration Risk:**  
Because `role` lives on the primary auth table, a failed migration in production could lock users out. Mitigation: always run `migrate --check` in CI before deployment, and keep `role` nullable with a safe default (`"viewer"`) so rollback does not corrupt existing sessions.
