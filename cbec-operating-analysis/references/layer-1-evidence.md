# Layer 1 Evidence

Layer 1 is deterministic. Prefer Python scripts over prompt-only transformations.

Assume execution from the agent's current project root unless the user explicitly gives different paths.

Read [workflow_contract.md](workflow_contract.md) before running the full chain.

## Objective

Export evidence tables that let later layers answer:

- What is the company-level budget gap?
- Is the problem scale or unit economics?
- Which channels, regions, categories, and models drive the gap?
- Which business subjects explain the profit shortfall?

## Directory contract

Write evidence under:

- `<run_root>/run_context/`
- `<run_root>/evidence/workbook/`
- `<run_root>/evidence/company/`
- `<run_root>/evidence/structure/`
- `<run_root>/evidence/refund/`
- `<run_root>/evidence/model/`

The standard run root is:

- `output/runs/<YYYYMMDD-HHMMSS-XX>/`

This avoids overwriting previous reports and keeps each run auditable.

Default script locations:

- `skills/cbec-operating-analysis/scripts/ensure_environment.py`
- `skills/cbec-operating-analysis/scripts/generate_evidence.py`
- `skills/cbec-operating-analysis/scripts/generate_operating_report.py` as the current project-specific baseline

## Stage 0 outputs

Generate these before exporting full evidence:

- `environment_check.md`
- `dependency_status.json`
- `workbook_profile.md`
- `field_mapping_draft.md`
- `header_index.json`

## Recommended evidence files

### Company

- `company_kpi_mtd.csv`
- `company_kpi_ytd.csv`
- `company_profit_bridge_mtd.csv`
- `company_profit_bridge_ytd.csv`
- `company_gmv_price_volume_mtd.csv`
- `company_gmv_price_volume_ytd.csv`

### Structure

- `channel_mix_ytd.csv`
- `region_mix_ytd.csv`
- `category_mix_mtd.csv`
- `channel_region_profit_variance_mtd.csv`
- `category_channel_profit_variance_mtd.csv`
- `category_monthly_trend_top10.csv`
- `category_monthly_trend_selection.csv`

### Refund

- `refund_by_channel_category_mtd.csv`
- `refund_by_channel_region_mtd.csv`
- `refund_company_summary_mtd.csv`

### Model

- `model_profit_bridge_mtd.csv`
- `model_profit_bridge_ytd.csv`
- `loss_models_mtd.csv`
- `loss_models_ytd.csv`

### Anomaly candidates

- `anomaly_candidates.csv`
- `channel_region_risk_flags.csv`
- `category_channel_risk_flags.csv`
- `model_root_cause_candidates.csv`

### Signal board

Recommended:

- `output/analysis/00_signal_board.md`

This file should summarize what looks unusual before the full final report is written.

### Trend-series rule

For category trend charts:

- first rank categories by current-month GMV
- if category count is large, keep the top 10 current-month categories
- export monthly GMV and gross margin trend data for those categories
- export a short selection file that recommends which 1-3 charts deserve the final report

## Required fields

Use consistent column names whenever possible:

- `period`
- `dimension`
- `subdimension`
- `model`
- `actual_value`
- `budget_value`
- `last_year_value`
- `variance_vs_budget`
- `yoy_variance`
- `actual_rate`
- `budget_rate`
- `last_year_rate`
- `variance_rate_vs_budget`
- `variance_rate_yoy`
- `profit_impact`
- `driver_type`
- `driver_rank`

## Business subject mapping

Keep these mappings stable:

- logistics headship = budget `预算头程成本 + 预算二程配送费 + 预算关税`
- logistics overseas = budget `预算海外仓费用`, actual `海外仓费用`
- delivery fee = budget `预算FBA配送费 + 预算FBM配送费`, actual `订单FBA费用`
- other platform fee = budget `预算平台其他费用 + 预算异常费用`, actual `其他费用合计`

If a source sheet cannot fully support a split, export the closest supported field and record the limitation in the report header.

## Validation rules

Before using evidence in analysis:

- required dependencies should be checked before chart generation
- company-level bridge must close back to total gross profit variance
- price-volume decomposition must close back to total GMV variance
- subgroup sums should reconcile to company totals within rounding tolerance
- if an actual field has no budget counterpart, mark it explicitly instead of inferring silently

## Environment rule

The standard workflow should attempt dependency installation when required packages are missing.

Missing plotting support is not a valid reason to silently replace the chart layer with a weaker final output path.

## Profiling step

Before exporting full evidence, profile the workbook:

- sheet names
- header rows
- likely semantic mappings
- fields requiring confirmation

Write this under `output/evidence/workbook/`.
