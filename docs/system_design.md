# System Design - OPRA.AI Automotive MVP

* **Purpose:** Define the approved software architecture, module boundaries, data contracts, configuration, execution flow, and quality constraints for OPRA.AI.
* **Scope:** OPRA.AI Version 1 modular pipeline monolith.
* **Status:** Approved
* **Version:** 1.0
* **Last Updated:** 2026-11-23
* **Owner:** Product and Engineering Lead
* **References:** `AGENTS.md`, `docs/product_requirements.md`, `docs/mvp_scope.md`

---

## 1. Overview

OPRA.AI is a data-driven operational decision-support platform for automotive service centers and repair garages. Version 1 transforms local CSV records into validated operational data, comparable KPI results, deterministic findings, evidence-backed recommendations, and structured reports.

The MVP uses a modular monolith rather than distributed services. This keeps the analytical core testable and deployable as a single Python application while preserving clear module boundaries for later extraction or UI/API integration.

## 2. Goals

The system design must enable the following goals:

* Accept operational records through a local CSV interface.
* Validate and normalize records without silently discarding invalid data.
* Calculate documented KPIs for comparable reporting periods.
* Evaluate KPI results against configurable, explainable thresholds.
* Produce findings and recommendations linked to supporting evidence.
* Export deterministic JSON and human-readable Markdown reports.
* Preserve pure core logic independent of filesystems, networks, and environment variables.
* Provide a clear CLI contract and reliable exit codes.

## 3. Non-Goals

Version 1 does not include:

* A web application or public HTTP API.
* Live database synchronization.
* Machine-learning models or probabilistic predictions.
* Autonomous changes to operational systems.
* Causal diagnosis that is not supported by the available data.
* Multi-tenant authentication or role-based access control.
* Multi-industry business rules.
* Distributed processing or microservices.

MongoDB is not part of the approved MVP data pipeline. CSV remains the Version 1 source of truth.

## 4. Architectural Style

OPRA.AI v1 is a **modular pipeline monolith** implemented in Python. Stages execute sequentially, and each stage depends only on typed objects and lower-level shared contracts.

```text
+---------------+    +----------------------+    +-------------------+
|   Ingestion   | -> | Validation/Cleaning  | -> | Analytics/KPI     |
|   (CSV I/O)   |    | (Typed normalization)|    | Engine            |
+---------------+    +----------------------+    +-------------------+
                                                       |
                                                       v
+------------------+    +----------------------+    +-------------------+
| Reporting        | <- | Recommendations      | <- | Findings          |
| (JSON / Markdown)|    | Engine               |    | Engine            |
+------------------+    +----------------------+    +-------------------+
```

Data flows in one direction through the pipeline. The only data returned backward is a report containing status, warnings, rejected records, findings, and recommendations.

## 5. Package and Module Layout

```text
src/
`-- opra/
    |-- __init__.py
    |-- config.py
    |-- exceptions.py
    |-- models/
    |   |-- records.py
    |   |-- analytics.py
    |   `-- intelligence.py
    |-- ingestion/
    |   `-- csv_loader.py
    |-- validation/
    |   `-- validator.py
    |-- analytics/
    |   |-- periods.py
    |   `-- kpi_engine.py
    |-- intelligence/
    |   |-- rules.py
    |   `-- recommender.py
    |-- reporting/
    |   |-- json_exporter.py
    |   `-- md_exporter.py
    `-- cli.py

tests/
|-- unit/
`-- integration/

examples/
`-- automotive/
```

## 6. Component Responsibilities

| Module | Allowed responsibilities | Forbidden responsibilities |
|---|---|---|
| `config` | Typed configuration and analytical thresholds | Reading operational CSVs or environment state directly |
| `models` | Immutable domain types and report schemas | Business logic and I/O |
| `ingestion` | CSV reading, encoding checks, header verification, raw row emission | KPI calculations or silent row filtering |
| `validation` | Type conversion, range and enum checks, normalization, rejection reporting | Direct file I/O or recommendation generation |
| `analytics` | Period slicing, KPI formulas, variance calculations | File I/O or threshold alerting |
| `intelligence` | Finding evaluation and recommendation mapping | Recalculating KPIs or changing metric values |
| `reporting` | JSON and Markdown serialization | Filtering data or applying business rules |
| `cli` | Argument parsing, configuration loading, pipeline orchestration, output writing | Analytical formulas or validation rules |

## 7. Core Design Principles

### 7.1 Pure core logic

The validation, analytics, and intelligence modules must operate on in-memory typed objects. They must not read files, make network requests, or access environment variables.

### 7.2 Immutability

Validated records passed to analytics must not be mutated in place. Each pipeline stage may return a new typed result or collection.

### 7.3 Explicit contracts

Stages communicate through dataclasses or Pydantic models. List and dictionary structures must not replace domain models when a named contract is available.

### 7.4 Explicit errors

Domain failures belong to `exceptions.py`, such as:

* `SchemaValidationError`
* `InsufficientDataError`
* `ConfigurationError`

Generic `Exception` and unexplained `ValueError` raising are not appropriate for pipeline errors.

### 7.5 Configuration-driven thresholds

Rules and thresholds live in typed configuration, for example:

* `revenue_drop_alert_pct`
* `min_sample_size`
* `turnaround_spike_pct`

Defaults must be documented and support controlled overrides.

### 7.6 Determinism

For the same input records and configuration, JSON output must be stable enough for repeatable testing. Ordering, serialization, and recommendation ranking must be deterministic.

## 8. Data Contracts

### 8.1 Raw job record

The ingestion stage emits raw row dictionaries and header metadata. It must not silently reinterpret or discard a row.

Required fields are governed by the MVP product requirements. Invalidation of a field must produce a validation issue tied to the row and field.

### 8.2 Validated job record

`ValidatedJobRecord` represents one normalized automotive operational record after validation.

Representative fields:

* `job_id` (unique identifier).
* `vehicle_id` (anonymized vehicle identifier).
* `customer_id` (anonymized identifier for repeat-visit tracking).
* `service_category`.
* `job_status` (`completed`, `in_progress`, `cancelled`).
* `intake_date` and `completion_date`.
* `labor_revenue`, `parts_revenue`, and `total_revenue`.
* `labor_hours` (optional/nullable).

The authoritative field definitions are in `docs/product_requirements.md` section 1. Turnaround time is derived from `intake_date` and `completion_date` by the analytics stage and is not stored on the record.

Currency and units must be normalized or explicitly rejected according to configuration.

### 8.3 Validation issue

`ValidationIssue` contains:

* Row number.
* Field name.
* Rejection or warning category.
* Human-readable reason.
* Original value, if safe to retain.

The validation stage may return valid records and issues in a single result rather than throwing for an isolated bad row.

### 8.4 Period window

`PeriodWindow` identifies the start and end of one comparison period. It must define inclusive or exclusive boundaries explicitly.

### 8.5 KPI result

`KPIResult` contains:

* KPI name or stable identifier.
* Current-period value.
* Comparison-period value, if applicable.
* Absolute and percentage variance, if applicable.
* Record count or sample size.
* Measurement unit.
* Qualification status, for example insufficient data.

No denominator may be treated as zero without an explicit result.

### 8.6 Finding

A `Finding` links threshold evaluation to evidence:

* Stable finding identifier.
* Finding type.
* Severity.
* Description.
* Related KPI identifiers.
* Supporting values.
* Applicable period.
* Sample size (`n` jobs evaluated).
* Low-confidence flag, set when the sample size falls below `min_sample_size`.

Findings must describe observed results rather than unverified causal claims.

### 8.7 Recommendation

A `Recommendation` contains:

* Stable recommendation identifier (`recommendation_id`).
* Title.
* Source finding identifier (`finding_id`).
* Evidence summary.
* KPI references.
* Severity.
* Priority.
* Suggested action.
* Confidence level.
* Limitations.
* Affected operational area.

The recommender must not generate a recommendation that has no linked finding.

### 8.8 Analysis report

`AnalysisReport` is the top-level typed output:

* Report metadata.
* Source dataset summary.
* Validation summary.
* Period definitions.
* KPI results.
* Findings.
* Recommendations.

## 9. Pipeline Execution

The CLI orchestrates the pipeline in this order:

1. Parse command-line arguments.
2. Load typed configuration and apply supported overrides.
3. Verify the input and output paths.
4. Load and inspect the CSV.
5. Validate headers and normalize records.
6. Separate valid records from rejected and warning rows.
7. Establish comparison periods.
8. Calculate KPI results.
9. Evaluate findings.
10. Map findings to recommendations.
11. Build `AnalysisReport`.
12. Export JSON and/or Markdown.
13. Report validation warnings and set a meaningful exit code.

### 9.1 Pipeline result

The pipeline should keep execution status separate from report data:

* Successful output.
* Partial success due to rejected rows.
* Configuration or schema failure.
* Insufficient data for comparison.
* I/O failure.

## 10. Analytics Rules

### 10.1 Period slicing

Period comparison must be driven by configuration or validated CLI options. The implementation must exclude records outside the selected window and avoid comparing periods of unequal meaning.

### 10.2 KPI calculation

Each KPI function must:

* Accept validated records and a typed period definition.
* Return a typed `KPIResult`.
* Use an explicit formula.
* Handle empty periods and zero denominators.
* Avoid mutating input records.

### 10.3 Variance calculation

Percentage variance must be reported only when the base value is defined and non-zero. Absolute variance may still be available where safe. Insufficient data must produce qualification metadata rather than an artificial value.

### 10.4 Minimum sample size

Findings based on small samples must be suppressed or explicitly qualified according to `min_sample_size`.

## 11. Configuration

Configuration must include:

* Revenue and cost field names.
* Date field name and accepted date format.
* Currency and numeric precision.
* Minimum sample size.
* Finding thresholds.
* Output formats.
* Default output directories.

Configuration errors must include the setting name and a remediation message.

Environment variables may configure runtime paths or secrets in a future integration. They must not be read by pure core modules.

## 12. CLI Contract

The CLI is a thin orchestration layer.

### 12.1 Expected behavior

The CLI must:

* Accept an input CSV path.
* Accept an output directory.
* Accept supported format and period options.
* Print concise status to standard output.
* Print actionable errors to standard error.
* Use non-zero exit codes for configuration, schema, or I/O failures.

### 12.2 Exit codes

| Exit code | Meaning |
|---|---|
| `0` | Report generated successfully |
| `1` | Unexpected operational failure |
| `2` | Invalid arguments or configuration |
| `3` | CSV schema or required-header failure |
| `4` | Insufficient data for a required comparison |

## 13. Error Handling

Error handling follows these rules:

* I/O errors belong in ingestion or the CLI boundary.
* Row-level issues belong in validation results.
* Formula and period failures belong in analytics exceptions or qualified results.
* Rule evaluation failures belong in intelligence exceptions.
* Export failures belong in reporting or the CLI boundary.
* Domain exceptions must not expose internal stack traces to normal CLI users.

## 14. Reporting

### 14.1 JSON report

The JSON exporter must produce a complete, machine-readable representation of `AnalysisReport`. Output should use stable field names and ISO-8601 values where dates are serialized.

### 14.2 Markdown report

The Markdown exporter must present:

* Report summary.
* Input and validation summary.
* KPI results.
* Findings.
* Recommendations.
* Data limitations and insufficient-data notices.

Reports must not claim stronger certainty than the evidence supports.

## 15. Security and Privacy

Version 1 processes local CSV data. The system must:

* Avoid logging raw sensitive records by default.
* Keep database credentials and API secrets outside source control.
* Support `.env` files for local configuration only.
* Validate paths and reject unsafe output destinations where applicable.
* Remove credentials from serialized reports.
* Provide no public data ingestion endpoint.

MongoDB URI credentials used for exploratory scripts must not be committed to the repository.

## 16. Testing Strategy

### 16.1 Unit tests

Unit tests cover:

* Schema and row validation.
* Date, numeric, enum, and range edge cases.
* Zero denominators.
* Empty periods.
* Period slicing.
* KPI formulas.
* Threshold boundaries.
* Finding and recommendation mappings.
* JSON and Markdown serialization.

### 16.2 Integration tests

Integration tests cover the complete CSV-to-report pipeline using synthetic automotive data. They verify:

* Valid CSV processing.
* Partial success with rejected rows.
* Invalid headers.
* Insufficient comparison data.
* Repeatable report output.
* CLI exit codes.

### 16.3 Test fixtures

Synthetic fixtures must contain no real customer or vehicle information.

## 17. Quality Gates

Before merge or release:

* Unit and integration tests pass.
* Code formatting passes.
* Static linting passes.
* Type checking passes.
* No secrets or credentials are present in source or fixtures.
* Core modules have no I/O or environment dependencies.
* Documentation matches implemented commands and data contracts.

## 18. Observability

Version 1 is primarily local and CLI-based. Minimum operational visibility includes:

* Input row and valid row counts.
* Rejected and warning row counts.
* Selected period boundaries.
* Calculated KPI identifiers.
* Pipeline stage completion status.
* Non-sensitive error summaries.

Verbose diagnostics must be opt-in and must not expose database credentials or full sensitive records.

## 19. Deployment

The MVP is a local Python application. Deployment requirements are:

* A supported Python virtual environment.
* Declared dependencies in `requirements.txt`.
* Read access to the input CSV.
* Write access to the output directory.
* Optional local `.env` configuration.

The modular monolith can later be packaged as a CLI executable or hosted behind an API without changing core analytics contracts.

## 20. Extensibility

Future work may add:

* Database-backed ingestion.
* REST or MCP interfaces.
* Additional industries.
* External data sources.
* Visualization dashboards.
* User authentication and authorization.
* Scheduled report generation.
* Alert delivery.

These integrations must depend on core domain contracts rather than bypassing validation or KPI modules.

## 21. Architecture Decision Records

### ADR-001: Modular pipeline monolith

* **Decision:** Implement OPRA.AI as a modular pipeline monolith.
* **Reason:** The MVP requires clear separation and testability without distributed-service complexity.
* **Consequences:** A future interface or persistence layer can be added at the boundaries.

### ADR-002: CSV as MVP input

* **Decision:** Use CSV files for Version 1 ingestion.
* **Reason:** CSV provides a low-friction, auditable source for garage operational data.
* **Consequences:** Live integrations and streaming ingestion are intentionally deferred.

### ADR-003: Deterministic rules

* **Decision:** Use configured rules and threshold comparisons instead of machine learning.
* **Reason:** MVP findings must be explainable and reproducible.
* **Consequences:** Findings are limited to conditions represented in the available data.

## 22. Implementation Readiness Checklist

* [ ] Directory structure matches this design.
* [ ] Domain models are implemented in `models/`.
* [ ] CSV ingestion and header validation are implemented.
* [ ] Validation issues preserve row and field context.
* [ ] Period and KPI engines are pure and typed.
* [ ] Finding rules consume KPI results only.
* [ ] Recommendations reference linked findings.
* [ ] JSON and Markdown exporters use `AnalysisReport`.
* [ ] CLI orchestration is thin.
* [ ] Unit and integration test suites satisfy quality gates.
* [ ] No credentials or live customer data are committed.
