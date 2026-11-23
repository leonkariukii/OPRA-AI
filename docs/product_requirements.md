# Product Requirements Document (PRD) — OPRA.AI Automotive MVP

* **Purpose:** Specify verifiable functional and non-functional requirements for OPRA.AI v1.
* **Scope:** Automotive garage operational analytics MVP.
* **Status:** Approved
* **Version:** 1.0
* **Last Updated:** 2026-11-23
* **Owner:** Product & Engineering Lead
* **References:** `docs/project_overview.md`, `docs/mvp_scope.md`, `docs/system_design.md`

---

## 1. Core Automotive Job Record Domain

For the MVP, the primary unit of operational analysis is a **Service Job Record** representing a vehicle service order/job card with attributes including:
* `job_id` (unique identifier)
* `vehicle_id` or anonymized vehicle identifier
* `customer_id` (anonymized identifier for repeat-visit tracking)
* `service_category` (e.g., Routine Maintenance, Diagnostics, Brake & Suspension, Engine & Transmission, Electrical, Body & Tires)
* `job_status` (`completed`, `in_progress`, `cancelled`)
* `intake_date` and `completion_date`
* `labor_revenue`, `parts_revenue`, and `total_revenue`
* `labor_hours` (optional/nullable)

---

## 2. Functional Requirements (FR)

### Stage 1: Data Ingestion & Validation
* **FR-001 (CSV Ingestion):** The system shall ingest UTF-8 CSV files containing automotive service job records and parse them into typed internal structures.
* **FR-002 (Schema Validation):** The system shall verify the presence of all required columns before processing and fail fast with an explicit, structured error listing missing columns if the schema is invalid.
* **FR-003 (Row-Level Data Validation):** The system shall validate each record for data types, non-negative monetary values, valid ISO date formats, valid `job_status` values, and logical date order (`completion_date >= intake_date`).
* **FR-004 (Validation Reporting):** The system shall separate valid records from rejected/quarantined records and produce a validation summary detailing total rows, valid rows, rejected rows, and specific failure reasons per row.

### Stage 2: Normalization & Period Partitioning
* **FR-005 (Data Normalization):** The system shall standardize string casing/whitespace on categorical fields (`service_category`, `job_status`) and normalize dates for period grouping.
* **FR-006 (Reporting Period Filtering):** The system shall partition validated records into explicit, comparable reporting periods (e.g., current period vs. prior period of equal duration) based on `completion_date` for completed jobs.

### Stage 3: Automotive KPI Analytics
* **FR-007 (Revenue KPIs):** The system shall calculate:
  * Total Completed Revenue
  * Revenue Breakdown by `service_category` (amount and percentage share)
  * Labor vs. Parts Revenue Split
  * Average Revenue per Completed Job (Average Ticket Size)
* **FR-008 (Operational Throughput KPIs):** The system shall calculate:
  * Total Jobs Intake vs. Completed vs. Cancelled
  * Job Completion Rate (`completed / total non-cancelled` or clearly defined formula)
  * Average & Median Job Turnaround Time (days/hours from `intake_date` to `completion_date`)
* **FR-009 (Customer Retention KPIs):** The system shall calculate:
  * Repeat Customer Rate (share of distinct `customer_id`s with `> 1` completed job in the evaluation window)
* **FR-010 (Period-over-Period Comparison):** The system shall compute absolute variance and percentage change for each KPI between two comparable reporting periods, safely returning `None` when the baseline period value is zero or missing.

### Stage 4: Deterministic Findings Engine
* **FR-011 (Threshold & Rule Evaluation):** The system shall evaluate calculated KPIs against documented analytical rules (e.g., category revenue drop exceeding configured threshold, turnaround time spike, high cancellation rate, low repeat customer rate) to generate structured `Finding` objects.
* **FR-012 (Sample Size & Data Quality Qualification):** Every `Finding` shall attach sample-size metadata (`n` jobs evaluated) and flag low-confidence findings when sample size falls below the configured minimum threshold.

### Stage 5: Evidence-Backed Recommendation Engine
* **FR-013 (Traceable Recommendation Mapping):** The system shall map triggered `Finding` objects to structured `Recommendation` objects containing: `recommendation_id`, `title`, `finding_id`, `evidence_summary`, `kpi_references`, `severity`, `priority`, `suggested_action`, `confidence_level`, and `limitations`.
* **FR-014 (No Unsupported Claims):** Recommendations shall strictly reflect observed operational metrics and explicitly state analytical limitations (e.g., inability to infer external market factors from internal job logs).

### Stage 6: Report Generation
* **FR-015 (Structured Output Report):** The system shall export a complete analytical report (JSON and formatted Markdown summary) containing validation summary, KPI scorecard, period comparisons, triggered findings, and prioritized recommendations.

---

## 3. Non-Functional Requirements (NFR)

* **NFR-001 (Determinism):** Given identical input CSV data and configuration thresholds, the pipeline shall produce byte-for-byte identical KPI outputs, findings, and recommendations.
* **NFR-002 (Auditability):** Every reported number must be reproducible from the validated dataset using documented formulas.
* **NFR-003 (Performance):** The MVP pipeline shall process up to 50,000 service job records in under 5 seconds on standard local hardware.
* **NFR-004 (Modularity):** All core analytical modules shall run headless without network access, databases, or web servers.
* **NFR-005 (Privacy by Default):** The system shall not require customer names, phone numbers, emails, or license plates to execute core analytics.