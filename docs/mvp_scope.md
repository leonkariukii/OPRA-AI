# MVP Scope Definition — OPRA.AI Version 1

* **Purpose:** Establish unambiguous boundaries between what will be built in Version 1 and what is explicitly excluded.
* **Scope:** OPRA.AI Automotive MVP.
* **Status:** Approved
* **Version:** 1.0
* **Last Updated:** 2026-11-23
* **Owner:** Product & Engineering Lead
* **References:** `AGENTS.md`, `docs/product_requirements.md`, `docs/system_design.md`

---

## 1. MVP Objective

Deliver an end-to-end, local/CLI-executable analytical engine that ingests automotive garage CSV job records, validates data quality, computes core operational and financial KPIs across comparable periods, identifies rule-based operational findings, and outputs prioritized, evidence-backed recommendations in JSON and Markdown formats.

---

## 2. In Scope (Version 1)

* **Domain:** Automotive repair garages and vehicle service centers only.
* **Data Source:** Single-table or normalized CSV file ingestion of service job records.
* **Validation Layer:** Schema validation, type checking, date consistency rules, and quarantine/error reporting for malformed rows.
* **Analytics Engine:**
  * Historical descriptive and comparative analytics (Current Period vs. Prior Period).
  * Core automotive KPIs: Revenue, Category Mix, Labor/Parts Split, Average Ticket Size, Job Volume, Completion/Cancellation Rates, Turnaround Time, Repeat Customer Rate.
* **Intelligence & Recommendations:**
  * Deterministic, threshold-driven rules engine for findings.
  * Structured, rule-mapped recommendations with confidence levels and explicit limitations.
* **Output:** Programmatic Python API, CLI runner, and structured JSON + Markdown report export.
* **Testing & Governance:** Comprehensive unit/integration test suite using synthetic garage datasets.

---

## 3. Out of Scope (Strictly Prohibited in Version 1)

AI agents and developers must **not** build any of the following during MVP execution:

1. **Multi-Industry Support:** No generic plugin marketplaces, retail/healthcare/logistics schemas, or abstract multi-vertical frameworks.
2. **Generative AI / LLM Integrations:** No OpenAI/Anthropic/Gemini API calls for generating findings, rewriting recommendations, or conversational chat interfaces.
3. **Predictive Forecasting / ML Models:** No demand forecasting, churn prediction models, or anomaly-detection neural networks; v1 is strictly historical and rules-based.
4. **Web Frontend / Mobile App:** No React/Next.js dashboard, mobile UI, or interactive visualization frontend in v1.
5. **Authentication & Multi-Tenancy:** No user login, RBAC, OAuth, JWTs, or tenant isolation databases.
6. **Live Third-Party Connectors:** No direct API integrations with QuickBooks, Xero, WhatsApp, SMS gateways, or external garage POS systems.
7. **Database Persistence Layer:** No PostgreSQL/SQLite persistence requirement for core MVP execution; pipeline operates cleanly in memory from CSV to report artifact.
8. **Payments & Subscriptions:** No billing, licensing, or SaaS metering logic.

---

## 4. Change Control

Moving any item from **Out of Scope** to **In Scope** requires an explicit scope amendment approved by the Project Owner before any implementation task is created.