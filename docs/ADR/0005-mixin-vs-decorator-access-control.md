# ADR 0005: Mixin vs Decorator for Access Control

**Status:** Accepted  
**Date:** 2026-05-01  
**Context:**  
We need to enforce access control across various views in the application. For instance, only authors can edit or delete their observations, and only rangers can verify observations. Django provides two primary mechanisms for access control on class-based views (CBVs): decorators (e.g., `@method_decorator(login_required)`) and mixins (e.g., `LoginRequiredMixin`, `UserPassesTestMixin`).

**Alternatives:**
1. **Mixins:** Inheriting from classes like `LoginRequiredMixin` and custom mixins to enforce checks in the view's dispatch method.
2. **Decorators:** Wrapping the view's `dispatch` method or URL routing with functional decorators.

**Decision:**  
We decided to use **Mixins** for access control across all Class-Based Views. Specifically, we use `LoginRequiredMixin` for general authentication, and custom mixins (`AuthorRequiredMixin` and `RangerRequiredMixin`) inheriting from `UserPassesTestMixin` for role and object-level checks.

**Code Reference:**  
- `echo_nt/observations/views.py:30` - `AuthorRequiredMixin` implementation.
- `echo_nt/observations/views.py:43` - `RangerRequiredMixin` implementation.

**Consequences:**  
- **Pros:** Mixins are the idiomatic approach for Class-Based Views in Django, resulting in cleaner and more readable code compared to stacking multiple `@method_decorator` calls. They also promote code reuse through inheritance.
- **Cons:** Mixin inheritance order is critical and can sometimes lead to subtle bugs if not ordered correctly (e.g., authentication mixins must precede view logic mixins).
