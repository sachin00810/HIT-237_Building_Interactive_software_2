# ADR 0005: Mixin vs Decorator for Access Control

**Status:** Accepted  
**Date:** 2026-05-01  
**Author:** Sachin

## Context
We need to enforce access control across various class-based views in the application. For instance, only authors can edit or delete their observations, and only rangers can verify observations. Django provides two primary mechanisms for access control on class-based views (CBVs): decorators (e.g., `@method_decorator(login_required)`) and mixins (e.g., `LoginRequiredMixin`, `UserPassesTestMixin`).

## Alternatives Considered

1. **Mixins:** Inheriting from classes like `LoginRequiredMixin` and custom mixins to enforce checks in the view's `dispatch()` method. This is the idiomatic CBV approach.
2. **Decorators:** Wrapping `dispatch()` or individual HTTP method handlers with `@method_decorator(login_required)` or `@method_decorator(permission_required(...))`.
3. **Function-Based Views with decorators:** Abandoning CBVs entirely in favour of FBVs where decorators feel more natural.

## Decision
We decided to use **Mixins** for access control across all Class-Based Views. Specifically:
- `LoginRequiredMixin` — ensures the user is authenticated before any view logic runs.
- `AuthorRequiredMixin` (custom, extends `UserPassesTestMixin`) — ensures only the observation's author can edit or delete it.
- `RangerRequiredMixin` (custom, extends `UserPassesTestMixin`) — ensures only users with `role == "ranger"` can verify observations.

**Code Reference:**
- `echo_nt/observations/views.py:30` — `AuthorRequiredMixin` definition
- `echo_nt/observations/views.py:43` — `RangerRequiredMixin` definition
- `echo_nt/observations/views.py:108` — `ObservationUpdateView` applying `AuthorRequiredMixin`
- `echo_nt/observations/views.py:148` — `ObservationVerifyView` applying `RangerRequiredMixin`

## Consequences

**Pros:**
- Mixins are the idiomatic CBV pattern in Django — readable, reusable, and composable.
- Logic is centralised: changing `AuthorRequiredMixin.test_func()` automatically applies to every view that inherits it.
- Cleaner than stacking multiple `@method_decorator` calls on each view class.

**Cons:**
- Python's Method Resolution Order (MRO) is critical — incorrect mixin ordering causes silent failures.
- Less intuitive to newcomers than function-based decorators.

## Security Implications

**Mixin Ordering — Privilege Escalation Risk:**  
The order of mixins in the class definition directly determines which check runs first. If `LoginRequiredMixin` is placed **after** `UserPassesTestMixin` in the MRO, an unauthenticated user could trigger `test_func()` before the login check, potentially causing an `AttributeError` or an incorrect permission result.

**Correct pattern (used throughout this project):**
```python
class AuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    ...
```
`LoginRequiredMixin` is always **leftmost**, ensuring unauthenticated users are redirected to login before `test_func()` is ever called. This eliminates the privilege escalation risk entirely.

**CSRF Protection on the Verify Endpoint:**  
The `ObservationVerifyView` (`echo_nt/observations/views.py:148`) only accepts `POST` requests, not `GET`. The verify form in `observation_detail.html` includes `{% csrf_token %}`, and Django's `CsrfViewMiddleware` (active in `settings.py:43`) validates the token on every non-safe HTTP method. This prevents Cross-Site Request Forgery attacks where an attacker's page could silently verify/unverify observations on behalf of a logged-in ranger.

**`raise_exception = True` on custom mixins:**  
Both `AuthorRequiredMixin` and `RangerRequiredMixin` set `raise_exception = True`. This ensures authenticated users who fail the permission check receive a `403 Forbidden` response (not a redirect to login), which is the semantically correct HTTP response and avoids leaking the existence of the login page as an escape route for permission bypasses.

