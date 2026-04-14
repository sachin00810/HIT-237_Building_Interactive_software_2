# HIT-237_Building_Interactive_software_2
Assignment 2 of HIT 237
# Echo NT - Interactive Fauna Observation App


This repository contains a Django web application built to track and manage fauna observations. This project emphasizes architectural decision-making, object-oriented design, and the practical application of Django design philosophies.

---

## 👥 Team Structure & Roles

This project was developed collaboratively by a team of four, with distinct responsibilities to ensure proper separation of concerns:

* **Member 1: Project Architecture & Setup Lead** *(Joshua Jnani)* **Focus:** Foundation, Core Structure, and System Architecture.  
    **Responsibilities:** Initialized the Django project, configured the `echo_nt` virtual environment, defined the app structure (`users`, `fauna`, `observations`), and managed base configurations.

* **Member 2: Models & Database Design Lead** *(Sachin Kharel)* **Focus:** Data Modelling, Object-Oriented Principles, and Relationships.  
    **Responsibilities:** Designed the ERD, implemented database schemas utilizing all three core relationships (`OneToOne`, `ForeignKey`, `ManyToMany`), and applied data encapsulation via the "Fat Models" philosophy.

* **Member 3: Views, Forms & Query Logic Lead** *(Muhammad Hassan)* **Focus:** Backend Logic, Class-Based Views (CBVs), and QuerySets.  
    **Responsibilities:** Built forms, implemented CBVs (ListView, DetailView, CreateView), and handled business logic using optimized QuerySet APIs (`select_related`, `prefetch_related`).

* **Member 4: Frontend, Integration & Documentation Lead** *(Saman Kandel)* **Focus:** User Interface, Template Integration, and Final Documentation.  
    **Responsibilities:** Designed responsive templates utilizing `base.html` inheritance, integrated frontend UI with backend views, and managed supplementary diagrams (ERD, Class diagrams).

---

## 🏗️ Architecture & Decision Records (ADRs)

In accordance with the assessment criteria, architectural decision-making is the core focus of this repository. We have documented every significant design choice in our **Architecture Decision Records (ADR)**.

You can find our living ADR document here:  
📄 `docs/ADR/0001-architecture.md`

**Key Philosophies Implemented:**
1.  **Fat Models, Thin Views:** Business logic (e.g., date-based observation validation) is encapsulated directly within the model classes rather than scattered across views.
2.  **Don't Repeat Yourself (DRY):** Extensive use of template inheritance (`base.html`) and Class-Based Views to eliminate redundant code.
3.  **Loose Coupling:** The project is strictly divided into three isolated apps (`users`, `fauna`, `observations`) that manage their own concerns.

---

## 🚀 Setup & Installation Guide

To run this Django application locally, follow these steps:

**1. Clone the repository**
```bash
git clone <your-github-repo-url>
cd <repository-folder>

    Group Plans for future assignments:
    