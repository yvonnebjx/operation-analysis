# Workflow Contract

This skill should behave like a staged operating-analysis pipeline, not a single opaque report generator.

## Run-directory rule

Every execution should live under a unique run root:

- `output/runs/<YYYYMMDD-HHMMSS-XX>/`

Where:

- `YYYYMMDD-HHMMSS` is the run timestamp
- `XX` is a sequence suffix inside the same second

Do not write final artifacts directly into a flat `output/` directory, because that will overwrite prior runs and break traceability.

## Standard stages

## Scope modes

### Full run

Run the entire chain when the user asks for:

- a complete operating analysis
- a final report
- a meeting or PPT package

### Partial run

Run only the minimum necessary stages when the user asks for a bounded artifact.

Common examples:

- `trend_charts`
  - outputs: top-category monthly trend evidence + charts + selection note
  - stages: 0, 1, 3
- `dashboard`
  - outputs: KPI dashboard cards and supporting KPI evidence
  - stages: 0, 1, 3
- `profit_bridge`
  - outputs: bridge and waterfall charts, plus bridge evidence
  - stages: 0, 1, 3
- `refund`
  - outputs: refund evidence, refund charts, optional short analysis note
  - stages: 0, 1, optional 2, 3
- `signal_board`
  - outputs: evidence + anomaly candidates + `00_signal_board.md`
  - stages: 0, 1, 2
- `final_report`
  - outputs: outline + final narrative using existing run outputs when possible
  - stages: 4, 5

Rule:

- when the request is narrow, do not produce unrelated deliverables
- when existing run outputs are sufficient, prefer reusing them instead of regenerating the entire chain
- if the user does not ask for a final report, do not write one by default

### Stage 0: Environment and workbook profiling

Objective:

- confirm the local Python environment can support the standard path
- identify workbook sheets, headers, and semantic mapping uncertainty

Required outputs:

- `<run_root>/run_context/environment_check.md`
- `<run_root>/run_context/dependency_status.json`
- `<run_root>/evidence/workbook/workbook_profile.md`
- `<run_root>/evidence/workbook/field_mapping_draft.md`
- `<run_root>/evidence/workbook/header_index.json`

Recommended:

- `<run_root>/run_context/period_context.json`

The run context should record how the target year-month was inferred from workbook coverage. Do not hardcode a month when the workbook clearly points to another latest period.

Checkpoint rule:

- if field ambiguity materially affects analysis, stop here and confirm with the user

### Stage 1: Evidence export

Objective:

- export mathematically closed evidence tables for KPI, bridge, structure, refund, and model analysis

Required outputs:

- company evidence CSVs
- structure evidence CSVs
- refund evidence CSVs
- model evidence CSVs
- `<run_root>/evidence/validation.md`

Structure evidence should include category monthly trend series for the top current-month categories when the category count is large.

### Stage 2: Risk pack

Objective:

- surface what is worth discussing before writing conclusions

Required outputs:

- `<run_root>/evidence/anomaly_candidates.csv`
- `<run_root>/evidence/channel_region_risk_flags.csv`
- `<run_root>/evidence/category_channel_risk_flags.csv`
- `<run_root>/evidence/model/model_root_cause_candidates.csv`

Recommended companion output:

- `<run_root>/analysis/00_signal_board.md`

### Stage 3: Visualization pack

Objective:

- generate enough charts to support a management review

Minimum chart scope:

- KPI dashboard cards for the target month
- company KPI comparison: MTD and YTD
- profit waterfall / bridge: MTD and YTD
- structure risk: at least channel-region and category-channel
- refund risk: by channel
- abnormal models: top negative models
- category trend charts: top 10 current-month categories by GMV

Required outputs:

- chart image assets under `<run_root>/charts/`
- `<run_root>/charts/chart_manifest.md`

### Stage 4: Outline pack

Objective:

- force the analysis into a meeting structure before full prose

Required outputs:

- `<run_root>/final/report_outline.md`
- `<run_root>/final/ppt_outline.md`

### Stage 5: Final narrative

Objective:

- produce the complete meeting-ready output

Required outputs:

- `<run_root>/final/management_report.md`
- `<run_root>/final/ppt_page_notes.md`

Writing rule:

- the final report should be shorter and more directional than the raw analysis notes
- the signal board and KPI dashboard should expose the main problem before detailed sections
- only 1-3 representative category trend charts should enter the final report, chosen from the trend selection file

Optional output:

- `<run_root>/final/management_review.pptx`

## Execution policy

- By default, complete all stages end-to-end.
- If the user explicitly wants a staged workflow, stop after each completed stage and ask whether to continue.
- Do not treat a fallback-only chart manifest as final success.
- Do not write the final report before the outline exists.
