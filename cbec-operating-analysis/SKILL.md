---
name: cbec-operating-analysis
description: Use when a user needs a cross-border ecommerce operating diagnosis rather than a fixed-format spreadsheet summary. Best for budget-vs-actual and YoY analysis across Amazon, Walmart, TikTok Shop, DTC, and similar channels, where the agent must map user-specific fields, generate reusable evidence slices, detect abnormal conditions, attribute business-category root causes, and produce a meeting-ready report and PPT outline with charts.
---

# CBEC Operating Analysis

This skill is for diagnosing operating risk from ecommerce business data. The goal is not to turn a fixed workbook into a fixed report. The goal is to help the agent:

1. understand the user's field meanings
2. infer the correct reporting period from workbook coverage
3. slice data into reusable evidence
4. detect abnormal conditions and high-value questions
5. produce management-grade conclusions
6. generate chart-backed report outputs

Assume the agent is running from the project root (`cwd`) unless the user says otherwise.

Default project conventions:

- workbook: `data/`
- runs base: `output/runs/`
- standard run root: `output/runs/<YYYYMMDD-HHMMSS-XX>/`
- evidence output: `<run_root>/evidence/`
- analysis output: `<run_root>/analysis/`
- final report output: `<run_root>/final/`
- chart output: `<run_root>/charts/`
- run context output: `<run_root>/run_context/`

Each run root must include a timestamp plus sequence suffix so a new run never overwrites an older report.

## Before any analysis

### 1. Standardize the local environment first

Open [references/workflow_contract.md](references/workflow_contract.md) first.

Run the environment check before charting or heavy analysis:

- `skills/cbec-operating-analysis/scripts/ensure_environment.py`

If a required dependency is missing, the default behavior is:

1. attempt installation from `skills/cbec-operating-analysis/requirements.txt`
2. if installation still fails, stop and surface the blocker clearly

Do not silently downgrade to a weaker visualization path in the standard workflow.

### 2. Read the mapping memory

Open [references/field_mapping_memory.md](references/field_mapping_memory.md) first.

Use it to:

- map workbook-specific fields to business meanings
- identify uncertain fields
- record confirmed meanings for future reuse

If a field is unclear and the answer materially affects analysis, ask the user to confirm it. After confirmation, update the mapping memory.

Also identify the latest usable reporting month from the workbook. Do not default to a hardcoded month when actual and budget sheets clearly cover a different period.

### 3. Read the business knowledge

Open only the references needed for the current case:

- [references/channel_knowledge.md](references/channel_knowledge.md)
- [references/seasonality_knowledge.md](references/seasonality_knowledge.md)
- [references/analysis_methodology.md](references/analysis_methodology.md)
- [references/report_outline_template.md](references/report_outline_template.md) when preparing the final writing depth

These references explain how to interpret channels, platform fee structures, seasonal effects, and what counts as an operating risk.

If the user provides a reference report in the project, use it to calibrate depth and meeting style. Treat it as a writing blueprint, not as a data template.

## Workflow

Follow the staged contract in [references/workflow_contract.md](references/workflow_contract.md).

Long chains may be executed in checkpoints when the user explicitly wants a staged run. Otherwise, proceed end-to-end.

## Execution modes

This skill supports two execution modes:

### 1. Full run

Use this when the user wants a complete operating review, such as:

- a full monthly management report
- a meeting-ready PPT outline
- a complete diagnosis with evidence, charts, and final narrative

Default behavior:

- run the full chain from Stage 0 to Stage 5

### 2. Partial run

Use this when the user asks for only part of the pipeline, such as:

- only monthly category trend charts
- only KPI dashboard cards
- only profit waterfall charts
- only refund analysis
- only anomaly candidate tables
- only the final report rewrite using existing outputs

Rule:

- only run the stages required for the requested output
- do not continue into later stages unless the user asks
- if the request is narrow, do not generate the full report by default

Examples:

- `只输出三级品类月度趋势图` -> Stage 0, Stage 1, Stage 3 only
- `只做当月利润瀑布图` -> Stage 0, Stage 1, Stage 3 only
- `只输出退款分析表和图` -> Stage 0, Stage 1, optional Stage 2, Stage 3
- `基于已有 evidence 重写最终报告` -> Stage 4 and Stage 5
- `完整跑一版经营分析汇报` -> Stage 0 to Stage 5

If the user request is ambiguous, infer the smallest reasonable scope first rather than defaulting to a full run.

### Stage 0 / Layer 1A: Environment and workbook profiling

Required outputs:

- `<run_root>/run_context/environment_check.md`
- `<run_root>/run_context/dependency_status.json`
- `<run_root>/evidence/workbook/workbook_profile.md`
- `<run_root>/evidence/workbook/field_mapping_draft.md`
- `<run_root>/evidence/workbook/header_index.json`

### Stage 1 / Layer 1B: Evidence generation

Use scripts to generate deterministic evidence. Do not let prompts invent calculations that should come from code.

Start with:

- `skills/cbec-operating-analysis/scripts/generate_evidence.py`

Read [references/layer-1-evidence.md](references/layer-1-evidence.md) before changing scripts or exporting evidence.

Outputs in this layer should include:

- company KPI tables
- profit bridges
- price-volume tables
- structure mix tables
- refund tables
- abnormal model tables
- anomaly candidate tables
- validation results

### Stage 2 / Layer 2: Analysis interpretation

Use AI to interpret evidence, not to replace evidence.

Read:

- [references/layer-2-analysis.md](references/layer-2-analysis.md)

Also follow:

- [references/report_spec.md](references/report_spec.md)

The agent should actively identify:

- proven risks
- structural anomalies
- abnormal products
- business-category root causes
- issues that still need department explanation

### Stage 3 / Layer 3A: Visualization pack

Generate charts only after evidence and anomaly tables exist.

Use:

- `skills/cbec-operating-analysis/scripts/generate_charts.py`

The standard chart pack should contain enough material for a management review, not only bridge charts.

### Stage 4 / Layer 3B: Outline-first delivery

Before writing the full report, first produce:

- `<run_root>/final/report_outline.md`
- `<run_root>/final/ppt_outline.md`

Use [references/report_outline_template.md](references/report_outline_template.md) and [references/report_spec.md](references/report_spec.md).

### Stage 5 / Layer 3C: Meeting-ready output

Write the full operating report and page-level notes after the outline is stable.

Read:

- [references/layer-3-ppt.md](references/layer-3-ppt.md)

The final writing should be done by the agent according to the report spec. Do not script fixed conclusion paragraphs.

## Root-cause rule

Within this skill, `root cause` should usually stop at management categories such as:

- volume shortfall
- selling price / mix deterioration
- discount deepening
- refund deterioration
- purchase cost deterioration
- headship deterioration
- overseas warehouse deterioration
- advertising deterioration
- commission deterioration
- delivery fee deterioration
- storage fee deterioration
- other platform cost deterioration
- structure shift

Do not jump directly to unsupported second-order causes like listing quality, warehouse staffing, or campaign setup unless the user provides evidence for them.

## Chart rule

Charts are required in the final layer. The specific rendering tool can vary. Prefer the simplest stable option available in the environment.

The preferred standard path is static chart generation under `output/charts/`.

If the plotting stack is missing, attempt dependency installation first. Fallback-only output is a non-standard debug path and should not be treated as a successful final delivery.

## Prompt templates

Use [references/prompt-templates.md](references/prompt-templates.md) for stable prompt scaffolding.

## Success condition

A successful run of this skill should leave behind:

- reusable evidence files
- reusable analysis markdown files
- a chart pack that is sufficient for management review
- a report outline
- a meeting-ready report
- a PPT outline
