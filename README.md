# OPRA.AI — Operational Performance & Recommendation Analytics

OPRA.AI is a data-driven business intelligence and operational decision-support platform designed to transform raw operational records into measurable KPIs, explainable analytical findings, and evidence-backed business recommendations.

The **Version 1 (MVP)** focuses on **automotive service centers and repair garages**, establishing a clean, modular analytical pipeline that can later generalize across other service industries.

---

## MVP Pipeline

```text
CSV Data Input ─▶ Schema & Rule Validation ─▶ Cleaning & Normalization ─▶ KPI & Trend Analytics ─▶ Rules-Based Findings ─▶ Evidence-Backed Recommendations ─▶ Structured Report

OPRA.AI/
├── README.md                  # Project overview, setup, and navigation
├── AGENTS.md                  # Mandatory rules and guardrails for AI coding agents
├── docs/
│   ├── project_overview.md    # Vision, problem statement, target users, value proposition
│   ├── product_requirements.md# Functional and non-functional requirements (FR/NFR)
│   ├── mvp_scope.md           # Explicit In-Scope and Out-of-Scope boundaries for v1
│   ├── system_design.md       # Modular monolith architecture and data flow
│   ├── agent_task_template.md # Standardized specification template for engineering tasks
│   └── quality_gates.md       # Definition of Done, test standards, and CI checks
├── src/
│   └── opra/                  # Core application source code
├── tests/                     # Automated unit and integration test suites
└── examples/                  # Synthetic automotive garage datasets for local testing
