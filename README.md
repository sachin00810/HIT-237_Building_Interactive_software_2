# EchoNT

EchoNT is a Django project for recording Northern Territory fauna observations. The repository is structured to emphasize architectural decision-making, object-oriented decomposition, custom managers, optimized QuerySets, and class-based view reuse.

## Core Features

- Northern Territory species catalogue with custom managers and queryset helpers
- Observation tracking built on Django generic class-based views
- Author-only update and delete flows through a reusable mixin
- Seed command for authentic NT fauna records
- ADR documentation for architectural decisions

## Project Structure

- `echo_nt/fauna/` contains catalogue models, managers, and seed command logic
- `echo_nt/observations/` contains observation models, forms, CBVs, and authorization mixins
- `echo_nt/users/` contains the custom user model required by settings
- `docs/ADR/` contains architecture decision records and the ADR template
- `supplementary_materials/` is reserved for ERDs and class diagrams

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply migrations:

```bash
python manage.py migrate
```

4. Seed the fauna catalogue:

```bash
python manage.py seed_nt_fauna --refresh
```

5. Start the development server:

```bash
python manage.py runserver
```

## Current Verification

The current codebase has been verified with:

```bash
python manage.py check
python manage.py migrate
python manage.py seed_nt_fauna --refresh
```

The list page, detail page, login page, and authenticated create/update flows all render successfully.

## Documentation Deliverables

- Project plan: `project_plan_and_contract.md`
- ADRs: `docs/ADR/`
- Supplementary materials placeholder: `supplementary_materials/README.md`

## Notes

- The local development database is intentionally ignored by git.
- Static placeholder files are explicitly preserved so the Django structure remains complete in GitHub.
