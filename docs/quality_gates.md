# Quality Gates & Definition of Done — OPRA.AI

* **Purpose:** Establish objective verification standards required before any task or pull request is accepted.
* **Scope:** All code, tests, and documentation changes in OPRA.AI.
* **Status:** Approved
* **Version:** 1.0
* **Last Updated:** 2026-11-23
* **Owner:** Product & Engineering Lead
* **References:** `AGENTS.md`, `docs/system_design.md`, `docs/agent_task_template.md`

---

## 1. Definition of Done (DoD)

A task is **NOT** complete merely because the script runs without crashing. Every deliverable must satisfy all applicable gates below:

1. **Requirement Traceability:** Every implemented behavior maps directly to an approved Requirement ID and Task ID.
2. **Scope Compliance:** Zero unapproved features, dependencies, or unrelated file modifications exist in the diff.
3. **Architectural Purity:** Core analytics and intelligence modules contain zero web, CLI, or database dependencies.
4. **Formula & Data Integrity:**
   * All KPI calculations match approved definitions.
   * Zero denominators are handled safely without `ZeroDivisionError`, `NaN`, or `Inf`.
   * Missing or malformed records are quarantined/reported explicitly rather than silently coerced.
5. **Automated Test Coverage:**
   * Unit tests exist for normal paths, empty inputs, zero baselines, invalid dates/amounts, and threshold boundaries.
   * 100% of automated tests pass (`pytest`).
6. **Static Analysis & Formatting:**
   * Linting passes with zero warnings/errors (`ruff check src/ tests/`).
   * Formatting conforms strictly (`ruff format --check src/ tests/`).
   * Static type checking passes with zero errors (`mypy src/`).
7. **Documentation Sync:** Any change to contracts, schemas, KPIs, or configuration is reflected in `docs/`.
8. **Diff & Limitation Review:** Full `git diff` reviewed and all known limitations disclosed in the completion report.

---

## 2. Mandatory Verification Commands

Run these checks locally and in CI before marking any task complete:

```bash
# 1. Run full test suite with coverage report on core package
pytest --cov=src/opra --cov-report=term-missing

# 2. Run linter
ruff check src/ tests/

# 3. Check code formatting
ruff format --check src/ tests/

# 4. Run static type checker
mypy src/