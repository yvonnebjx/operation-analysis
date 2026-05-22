# Report Spec

The final report must be written by the agent, not generated from fixed text templates in code.

## Authoring order

Write outputs in this order:

1. `<run_root>/final/report_outline.md`
2. `<run_root>/final/management_report.md`
3. `<run_root>/final/ppt_outline.md`
4. `<run_root>/final/ppt_page_notes.md`

## Required sections

1. Scope and data notes
2. KPI dashboard
3. Executive summary
4. Company P&L overview
5. Profit decomposition
6. Structural risks
7. Expense and refund risks
8. Abnormal models
9. Actions and open questions

## Depth target

Use a real management-review depth, not a table transcript.

The final report should:

- keep the mainline short and directional
- start with a dashboard-like KPI view before long tables
- elevate only the highest-value tables and anomalies
- point to evidence and charts explicitly
- distinguish proven conclusions from items awaiting business explanation

If the user provides a reference report, use it to calibrate section granularity and writing density.

## Writing rules

### Scope and data notes

State:

- how the target month was inferred from workbook coverage
- the period covered
- whether analysis is MTD, YTD, budget-vs-actual, and YoY
- any known field-mapping or data-split limitations

Never hardcode the reporting month when the workbook clearly covers a different latest month.

### KPI dashboard

Open with a compact board that lets the reader spot the issue immediately.

At minimum show:

- GMV
- gross profit or gross margin
- one profit-quality or risk indicator such as refund rate

Each KPI block should show:

- actual
- versus budget
- versus last year
- directional signal such as red/green up-down

### Executive summary

Must answer:

- what is off budget
- whether the issue is scale or unit economics
- what the top structural risks are

### Company P&L overview

Show current month and YTD with:

- actual
- budget
- variance vs budget
- last year
- YoY variance

Prefer compact tables. Do not dump all metrics into long transcript-style grids unless they change the management conclusion.

### Profit decomposition

Use bridges and price-volume logic to state which subjects drag profit most.

When explaining overall cost and profit movement, prefer a waterfall chart over simple ranking bars.

### Structural risks

Do not stop at ranking tables. State what structure is hurting profit:

- which channel shift
- which region shift
- which category x channel combination

When category count is high, support this section with selected category trend charts:

- trend charts should show monthly GMV as bars and gross margin as a line
- GMV and gross margin must appear in the same chart, using dual axes when needed
- do not split GMV and gross margin into separate charts
- generate charts for the top 10 current-month categories by GMV
- only place 1-3 abnormal or representative charts into the final report
- use the selection file from the evidence/chart layer instead of manually picking at random

### Refund risks

Must be channel-first, then category and region within channel.

### Expense and refund risks

This section should connect fee-rate pressure and refund pressure back to profit categories:

- advertising
- headship
- overseas warehouse
- commission
- delivery fee
- storage fee
- other platform fee
- refund

Do not leave fee items as isolated percentages if they materially explain profit variance.

### Abnormal models

Each model should have:

- abnormal attribution
- top negative drivers
- one short conclusion sentence

Keep the list short. The point is to expose the few models that require action, not to enumerate every weak SKU.

### Actions and open questions

Split into:

- immediate actions
- items requiring business explanation

## Tone

Use management language:

- concise
- evidence-backed
- directional

The reader should be able to identify the main problem and the required action within one screen.

Avoid generic filler and unsupported storytelling.
