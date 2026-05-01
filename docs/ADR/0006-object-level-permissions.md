# ADR 0006: Group-Based vs Object-Level Permissions

**Status:** Accepted  
**Date:** 2026-05-01  
**Context:**  
We need to manage permissions where certain actions apply broadly (e.g., rangers can verify any observation) and other actions apply strictly to specific records (e.g., only the original author can edit or delete an observation). We had to choose between using Django's built-in group and permission system versus implementing custom object-level permission logic.

**Alternatives:**
1. **Group-Based Permissions (Django Groups/Permissions):** Assigning users to groups ("Rangers") and granting global table-level permissions (e.g., "can_verify_observation").
2. **Object-Level Permissions with Custom Logic:** Implementing access checks directly in view mixins that evaluate the specific model instance and the requesting user's attributes (role or ID).
3. **Third-Party Packages (e.g., django-guardian):** Using a dedicated library for complex object-level permissions.

**Decision:**  
We decided to use **Object-Level Permissions with Custom Logic** via Mixins, bypassing the complexity of Django's group permission system for object-specific checks. The `role` field on the user model serves as a lightweight alternative to groups for broad authorization, while mixins inspect the specific object for ownership.

**Code Reference:**  
- `echo_nt/observations/views.py:34` - `AuthorRequiredMixin.test_func()` checks `self.get_object().user_id == self.request.user.id`.
- `echo_nt/observations/views.py:47` - `RangerRequiredMixin.test_func()` checks `self.request.user.role == "ranger"`.

**Consequences:**  
- **Pros:** Keeps the codebase lightweight and dependencies minimal. Permissions logic is highly visible directly in the views module. Avoids database queries to check group memberships.
- **Cons:** Custom logic must be manually applied to every relevant view or endpoint; there is no centralized database registry of who has what permission.
