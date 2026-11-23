
# OPRA.AI — Agent Engineering Guidelines

**Status:** Approved | **Version:** 1.0 | **Scope:** Global Repository Governance

---

## 1. Project Identity & Mission

* **Project:** OPRA.AI (Operational Performance & Recommendation Analytics)
* **MVP Domain:** Automotive repair garages and vehicle service operations.
* **Mission:** Build a reliable, maintainable, explainable, and extensible platform that turns structured operational data into accurate KPIs, traceable findings, and actionable recommendations.

---

## 2. Source of Truth Hierarchy

When documents conflict, do **not** silently pick one. Flag the conflict, explain its impact, and request resolution.

1. `docs/mvp_scope.md` & `docs/product_requirements.md` (Approved Requirements)
2. `docs/system_design.md` & ADRs (Approved Architecture)
3. Approved Data Dictionary & KPI Definitions
4. `docs/quality_gates.md` (Engineering & QA Standards)
5. `AGENTS.md` (This File)
6. Existing Codebase (Existing code is not automatically right simply because it exists)
7. Task-Specific Prompt Instructions

---

## 3. Scope Protection (Strict Prohibitions)

Agents and developers **MUST NOT** independently:

* Add features outside `docs/mvp_scope.md` or the assigned Task ID.
* Build multi-industry abstractions during the automotive MVP.
* Add LLMs/AI chat/forecasting models unless explicitly specified in an approved requirement.
* Introduce new web frameworks, ORMs, or third-party dependencies when existing tools suffice.
* Add authentication, billing, multi-tenancy, or external API integrations prematurely.
* Modify unrelated modules, rename public contracts, or refactor out-of-scope code during a task.

If you discover an improvement outside task scope, document it in your final report under **Follow-Up Recommendations**—do not implement it.

---

## 4. Mandatory Agent Execution Cycle

1. **INSPECT:** Read the Task Specification, `AGENTS.md`, relevant `docs/`, and existing code in affected modules.
2. **PLAN:** Output a concise implementation plan (affected files, logic approach, edge cases, test plan) and confirm scope alignment before editing files.
3. **IMPLEMENT:** Write minimal, modular, well-typed code strictly within task scope.
4. **VERIFY:** Run `pytest`, `ruff check`, `ruff format --check`, and `mypy`. Review the full `git diff`.
5. **REPORT:** Deliver the structured completion report defined in Section 8.

---

## 5. Architecture & Code Guardrails

* **Separation of Concerns:** Core validation, KPI analytics, finding rules, and recommendation logic must be pure Python functions/services with zero dependency on HTTP frameworks, CLI parsers, or database sessions.
* **Explicit Contracts:** Pass validated domain models/typed structures between pipeline stages rather than raw unvalidated dictionaries.
* **Python Standards:**
  * Require full type hints on all public functions and data structures.
  * Keep functions small and single-purpose.
  * Never swallow exceptions silently; raise explicit, descriptive domain errors.
  * Externalize all thresholds and environment settings into configuration—never hardcode magic numbers inside business logic.

---

## 6. Data, Analytics & Recommendation Integrity

* **Data Integrity:** Never silently drop rows, fabricate missing values, or coerce invalid numbers/dates into defaults without explicit validation rules and logging.
* **KPI Precision:**
  * Never invent or alter KPI formulas.
  * Guard all division operations against zero denominators (return explicit `None` or defined sentinel state, never `NaN`/`Inf` leaks).
  * Never compare incompatible or unequal reporting periods without explicit normalization.
  * Do not round intermediate values; round only at presentation/reporting boundaries.
* **Explainable Recommendations:**
  * Every recommendation must link directly to a triggered analytical finding, supporting metric values, severity/priority, suggested action, and explicit limitations.
  * Never state causation when data only shows correlation.
  * Never generate recommendations from insufficient sample sizes without flagging low confidence.

---

## 7. Security, Privacy & Testing

* Never commit secrets, API keys, credentials, or real customer PII. Use synthetic garage datasets for all development and tests.
* Every task requires unit tests covering: normal behavior, empty inputs, missing fields, zero denominators, invalid dates/amounts, and boundary thresholds.
* Never delete, skip, or weaken existing tests to make a change pass.

---

## 8. Mandatory Agent Completion Report

Every coding task must conclude with this exact report structure:

* **Summary:** Concise overview of what was built.
* **Files Changed:** List of created, modified, or deleted files.
* **Requirements Addressed:** Mapped Requirement IDs and Acceptance Criteria verified.
* **Tests Executed:** Commands run and pass/fail results.
* **Assumptions & Decisions:** Any design choices made within approved boundaries.
* **Limitations & Risks:** Known edge cases, incomplete items, or downstream impacts.
* **Follow-Up Recommendations:** Out-of-scope observations logged for future consideration.

---

## 9. Golden Rule

**When uncertain, do not invent.** Stop, cite the ambiguity in the documentation or data, and ask for clarification.