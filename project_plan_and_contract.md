# EchoNT Project Plan and Team Contract

## Project Overview
EchoNT is a Django application for recording Northern Territory biodiversity observations, managing fauna records, and demonstrating architectural quality through ADRs, OO decomposition, and optimized ORM usage.

## Team Roles
- Architecture and setup lead: Owns project structure, deployment configuration, and integration standards.
- Data modelling lead: Owns models, managers, encapsulation, migrations, and seed data quality.
- Backend logic lead: Owns CBVs, forms, queryset optimization, and authorization mixins.
- Frontend and documentation lead: Owns templates, UI integration, ERD/class diagrams, and final report polish.

## Delivery Scope
- Custom Django apps for `fauna`, `observations`, and `users`
- Authentic NT species catalogue and seeding workflow
- Observation CRUD powered by CBVs
- ADR pack documenting major decisions
- Supplementary ERD and UML class diagrams

## Working Agreement
- All architectural changes require an ADR update or a justified note in the pull request.
- Commits should stay focused to one concern or one file where practical.
- No merge-conflict markers may remain on `main`.
- Any view rendering related objects must justify its queryset strategy.
- Domain logic belongs in models, managers, querysets, or reusable mixins before being placed in views.

## Definition of Done
- `python manage.py check` passes
- Key files contain consistent imports and app configuration
- ADR references point to real files
- Seed command populates authentic Territory data
- Supplementary materials folder contains current ERD and class diagram exports

## Submission Checklist
- Repository URL verified
- `requirements.txt` committed
- ADR directory complete
- project plan and contract included
- supplementary materials uploaded
- final smoke test completed
