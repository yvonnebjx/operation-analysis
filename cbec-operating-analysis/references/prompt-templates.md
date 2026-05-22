# Prompt Templates

## Evidence export

Use when extending the Python layer:

```text
Use the workbook plus the field-mapping memory to export deterministic evidence tables for cross-border ecommerce operating analysis.

Requirements:
- first inspect headers and draft semantic mappings
- flag uncertain fields before full analysis
- keep budget and actual business subjects aligned
- export company, structure, refund, and model evidence
- export anomaly candidate tables instead of only final conclusions
- make all bridge tables mathematically close to total variance
- write outputs under the current `<run_root>/evidence/`
- write workbook profiling outputs before the full evidence pack
- export category monthly trend series for the top 10 current-month categories by GMV
- do not write narrative conclusions in this step
```

## Partial run routing

Use when the user asks for only one type of artifact:

```text
Interpret the request using the smallest valid scope.

Rules:
- if the user asks for charts only, do not generate the final report
- if the user asks for evidence only, do not generate charts or narrative
- if the user asks for a report rewrite using existing outputs, reuse the current run artifacts when possible
- if the user asks for a complete review, run the full pipeline

Typical scopes:
- trend_charts
- dashboard
- profit_bridge
- refund
- signal_board
- final_report
- full
```

## Management diagnosis

Use when converting evidence into markdown analysis:

```text
Read the evidence tables under `<run_root>/evidence/` and write a management operating analysis.

Requirements:
- separate proven conclusions from items that still need business explanation
- root causes should stop at management categories such as discount, refund, headship, overseas warehouse, advertising, commission, delivery fee, storage, other platform cost, structure shift, price/mix, and volume shortfall
- actively identify abnormalities worth discussing instead of summarizing every table
- write a short signal board before the long-form report
- for abnormal models, identify whether the issue is volume-led, unit-economics-led, or mixed
- write output files under `<run_root>/analysis/`
```

## Chart generation

Use when generating chart assets:

```text
Read `<run_root>/evidence/` and generate static chart assets for a management operating review.

Requirements:
- first verify the Python plotting environment and attempt dependency installation when required packages are missing
- write images under `<run_root>/charts/`
- prioritize KPI dashboard cards, waterfall charts, company KPI comparisons, structure charts, refund comparison charts, and abnormal model charts
- generate category trend charts for the top 10 current-month categories by GMV and produce a short selection note for the final report
- for category trends, use one combined dual-axis chart per category: GMV as bars and gross margin as a line
- standard success means a usable chart pack, not only a manifest
- do not silently downgrade to a fallback-only path
```

## Report outline

Use when generating the rough report structure:

```text
Based on `<run_root>/evidence/`, `<run_root>/analysis/`, and any user-provided reference report, draft a report outline for the monthly operating review.

Requirements:
- write the outline to `<run_root>/final/report_outline.md`
- keep the outline aligned with the report spec
- state which sections will use which evidence and charts
- decide which anomalies deserve full discussion and which should stay in appendix or notes
- keep the report tight enough that an operator can spot the main issue within one screen
```

## PPT outline

Use when generating the final deck structure:

```text
Based on `<run_root>/analysis/` and `<run_root>/charts/`, create a meeting-ready PPT outline for a monthly operating review.

Requirements:
- use short slide titles that already state the conclusion
- order slides from company summary to structure to abnormal products to actions
- end with a page of business follow-up questions grouped by owner
- write the outline to `<run_root>/final/ppt_outline.md`
```
