# ADR 0007: Session-Based vs Token-Based Authentication

**Status:** Accepted  
**Date:** 2026-05-01  
**Author:** Sachin

## Context

EchoNT requires a user authentication mechanism that protects views, enforces role-based access, and maintains identity across requests. Two primary authentication paradigms were evaluated: Django's built-in **session-based authentication** and **token-based authentication** (e.g., JWT — JSON Web Tokens). This decision underpins the entire auth architecture established in ADRs 0004–0006.

## Alternatives Considered

### Option 1: Session-Based Authentication (Django default)
Django stores an encrypted session identifier in a cookie (`sessionid`). On each request, the server looks up the session in the database, retrieves the associated user, and makes it available as `request.user`. The session record is invalidated on logout.

**Libraries:** Built into Django — `django.contrib.sessions`, `django.contrib.auth`

### Option 2: Token-Based Authentication (JWT)
A signed token (e.g., `eyJhbGciOiJSUzI1NiJ9...`) is issued at login and sent with every request in the `Authorization: Bearer <token>` header. The server validates the token's signature without hitting the database. Common libraries: `djangorestframework-simplejwt`, `python-jose`.

### Option 3: Hybrid — Sessions for Browser, Tokens for API
Maintain session auth for browser views while exposing a token-based REST API for future mobile or third-party clients. Adds complexity but maximises flexibility.

## Decision

We chose **Session-Based Authentication** (Option 1) for EchoNT.

**Code References:**
- `echo_nt/config/settings.py:29` — `django.contrib.sessions` in `INSTALLED_APPS`
- `echo_nt/config/settings.py:39` — `SessionMiddleware` in `MIDDLEWARE`
- `echo_nt/config/settings.py:42` — `AuthenticationMiddleware` attaches `request.user` from session
- `echo_nt/users/backends.py:1` — Custom `EmailOrUsernameBackend` plugs into Django's session auth pipeline

## Comparison

| Criterion | Session (chosen) | JWT / Token |
|---|---|---|
| **State** | Stateful — session record in DB | Stateless — all claims in token |
| **Revocation** | Instant — delete the session row | Hard — token valid until `exp` claim |
| **CSRF** | Auto-protected by `CsrfViewMiddleware` | Must implement manually (double-submit cookie or custom header) |
| **Server scalability** | Requires shared session store (e.g., Redis) in multi-server deployments | No shared store needed |
| **Mobile / API clients** | Poor fit — cookies not native to mobile | Excellent fit |
| **Implementation complexity** | Very low — fully built into Django | High — token issuance, refresh, blacklisting |
| **Security on logout** | Complete — session destroyed server-side | Incomplete — old token still valid until expiry |

## Consequences

**Pros:**
- Zero additional dependencies — sessions are a first-class Django feature.
- Logout is genuinely secure: `django.contrib.auth.logout()` deletes the session record, making the old session cookie useless immediately.
- `CsrfViewMiddleware` (active at `settings.py:43`) automatically protects all mutating endpoints (POST/PUT/DELETE) without any extra code.
- `request.user` is always available in views and templates — no token parsing required.

**Cons:**
- Every authenticated request hits the database to resolve the session (mitigated by database query caching and Django's session caching backends).
- Scaling to multiple servers requires a shared session store (e.g., Redis, Memcached). For EchoNT's single-server development deployment this is not a concern.
- Not suitable for a future REST API consumed by mobile clients — that would require revisiting this decision and adding token auth alongside sessions.

## Security Implications

**Session Fixation:**  
Django rotates the session ID on login (`django.contrib.auth.login()` calls `request.session.cycle_key()`), preventing session fixation attacks where an attacker pre-seeds a session ID.

**Session Hijacking:**  
The `sessionid` cookie is `HttpOnly` by default in Django, preventing JavaScript access. In production, `SESSION_COOKIE_SECURE = True` should be set to restrict the cookie to HTTPS connections only, preventing interception over plain HTTP.

**CSRF:**  
All POST views in EchoNT (create observation, verify observation, login, logout, password change) include `{% csrf_token %}` in their templates and are protected by `CsrfViewMiddleware`. This was a deliberate factor in choosing sessions over tokens — CSRF protection is automatic and requires no custom implementation.

**Brute Force Consideration:**  
Django's session auth does not include built-in rate limiting on login attempts. For a production deployment, `django-axes` or similar should be evaluated to lock accounts after repeated failed attempts. This is noted as a future improvement, not a current implementation.
