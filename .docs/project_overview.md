# Project Overview — OPRA.AI

* **Purpose:** Define the problem space, product vision, target users, and core value proposition of OPRA.AI.
* **Scope:** Strategic foundation for the OPRA.AI platform and its Version 1 automotive MVP.
* **Status:** Approved
* **Version:** 1.0
* **Last Updated:** 2026-11-23
* **Owner:** Product & Engineering Lead
* **References:** `README.md`, `AGENTS.md`, `docs/mvp_scope.md`, `docs/product_requirements.md`

---

## 1. Problem Statement

Small and mid-sized automotive garages generate daily operational data—job cards, service categories, labor hours, parts billed, turnaround times, and repeat visits—yet most owners run their businesses on intuition or static spreadsheets.

Key operational pain points include:
* **Blind Revenue Shifts:** Owners notice cash flow dips weeks late without knowing whether the drop came from fewer vehicles serviced, lower average ticket size, or declining high-margin service categories.
* **Unmeasured Workshop Bottlenecks:** Delayed vehicle turnarounds, stalled jobs, and technician utilization imbalances go untracked until customer complaints rise.
* **Data Without Action:** Generic accounting exports show totals, not operational diagnoses or concrete next steps.

---

## 2. Product Vision

**OPRA.AI (Operational Performance & Recommendation Analytics)** turns structured operational records into transparent, verifiable operational intelligence.

Rather than acting as a black-box dashboard, OPRA.AI answers three questions for business operators:
1. **What happened?** (Validated KPIs across comparable reporting periods)
2. **Why does it matter?** (Deterministic, rules-based operational findings)
3. **What should we do next?** (Prioritized, evidence-backed recommendations with clear limitations)

---

## 3. Target Users (Automotive MVP)

| Persona | Role | Primary Goal | How OPRA.AI Helps |
| :--- | :--- | :--- | :--- |
| **Garage Owner / Managing Director** | Business decision-maker | Protect margins, grow repeat revenue, spot operational leaks early | Period-over-period revenue & job mix diagnostics with prioritized action items |
| **Service Advisor / Workshop Manager** | Day-to-day floor operations | Reduce bay bottlenecks, improve job turnaround time, manage service demand | Turnaround time KPIs, stalled-job flags, and category throughput insights |
| **Operations Analyst / Consultant** | Advisor reviewing garage performance | Audit workshop health rapidly from exported CSV job logs | Standardized validation, reproducible KPI calculations, and exportable reports |

---

## 4. Core Value Proposition

* **Explainability Over Black Boxes:** Every finding and recommendation traces directly to exact source records and documented mathematical formulas.
* **Low-Friction Adoption:** Works directly with standardized CSV exports from existing garage management systems or spreadsheets—no complex hardware or live ERP integration required for MVP.
* **Honest Intelligence:** Explicitly surfaces sample-size limits, missing data warnings, and analytical uncertainty rather than fabricating insights.
* **Built to Generalize:** Designed around a clean separation between domain-specific schemas/rules (automotive v1) and the core analytical pipeline so future verticals can plug in cleanly.