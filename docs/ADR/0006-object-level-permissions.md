# ADR 0006: Group-Based vs Object-Level Permissions

**Status:** Accepted  
**Date:** 2026-05-01  
**Author:** Sachin

## Context
We need to manage permissions where certain actions apply broadly (e.g., rangers can verify any observation) and other actions apply strictly to specific records (e.g., only the original author can edit or delete their own observation). We had to choose between using Django's built-in group and permission system versus implementing custom object-level permission logic.

## Alternatives Considered

1. **Group-Based Permissions (Django Groups/Permissions):** Assigning users to groups (e.g., "Rangers") and granting global table-level permissions (e.g., `can_verify_observation`). Access checks would use `user.has_perm("observations.can_verify_observation")`.
2. **Object-Level Permissions with Custom Logic:** Implementing access checks directly in view mixins that evaluate the specific model instance and the requesting user's attributes (role or ID). No external database lookup required.
3. **Third-Party Package — `django-guardian`:** A mature library providing a full object-level permission framework backed by database rows. Supports `get_objects_for_user()` queries but adds a dependency and extra tables.
4. **Custom Middleware:** Intercept every request and evaluate permissions centrally. Powerful but overly complex for a 3-role application.

## Decision
We decided to use **Object-Level Permissions with Custom Mixin Logic**, bypassing Django's group permission system. The `role` field on `CustomUser` serves as a lightweight alternative to groups for broad authorization, while mixins inspect the specific model instance for ownership checks.

**Code Reference:**
- `echo_nt/observations/views.py:34` — `AuthorRequiredMixin.test_func()`: `self.get_object().user_id == self.request.user.id`
- `echo_nt/observations/views.py:47` — `RangerRequiredMixin.test_func()`: `self.request.user.role == "ranger"`
- `echo_nt/users/models.py:5` — `ROLE_CHOICES` defining the three roles

## Consequences

**Pros:**
- Keeps the codebase lightweight and dependency-free.
- Permission logic is highly visible — any developer reading the view class immediately understands the access rules.
- Avoids the extra database queries that Django's `user.has_perm()` requires (which hits the `auth_permission` and `auth_group` tables).

**Cons:**
- Custom logic must be manually applied to every relevant view — there is no centralised registry of permissions.
- If the application grows to require per-object permissions for many models, this approach would need to be migrated to `django-guardian` or similar.

## Security Implications

**IDOR (Insecure Direct Object Reference) Prevention:**  
Without `AuthorRequiredMixin`, any authenticated user who knows (or guesses) the primary key of another user's observation could access `/observation/42/update/` and modify it. This is a classic **IDOR vulnerability**.

`AuthorRequiredMixin.test_func()` at `echo_nt/observations/views.py:34` directly prevents this:
```python
def test_func(self):
    return self.get_object().user_id == self.request.user.id
```
The check compares the observation's `user_id` foreign key against the authenticated user's `id`. Even if an attacker enumerates PKs, they will receive a `403 Forbidden` response from `handle_no_permission()`. The object is fetched from the database (not from the URL) making URL manipulation ineffective.

**Why `django-guardian` was rejected:**  
`django-guardian` stores per-object permission assignments as database rows in `guardian_userobjectpermission`. For EchoNT's simple model — where ownership is already encoded in `Observation.user_id` — this would duplicate data we already have, add two extra tables, and require every query to join against permission rows. The complexity cost outweighs the benefit for a 3-role application with straightforward ownership semantics.

**Ranger Role — No Horizontal Escalation Risk:**  
Rangers can verify any observation but cannot edit or delete observations they do not own. `RangerRequiredMixin` only guards the verify endpoint; the update and delete endpoints are guarded separately by `AuthorRequiredMixin`. These two mixins are independent and cannot be combined to grant broader access than intended.

