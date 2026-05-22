# Layer 3 PPT

Layer 3 converts evidence and analysis into a meeting-ready final structure.

## Target outputs

Write under `output/final/`:

- `<run_root>/final/report_outline.md`
- `<run_root>/final/management_report.md`
- `<run_root>/final/ppt_outline.md`
- `<run_root>/final/ppt_page_notes.md`

Chart assets should live under:

- `<run_root>/charts/`

If slide generation is available, also produce:

- `<run_root>/final/management_review.pptx`

## Slide structure

Recommended order:

1. Cover
2. KPI dashboard
3. Executive summary
4. Scope and data notes
5. Company P&L summary: MTD and YTD
6. Profit decomposition: MTD
7. Profit decomposition: YTD
8. Structural risks: channel / region / category
9. Expense and refund risks
10. Loss models and abnormal attribution
11. Actions and required business explanations

## Slide rules

- one message per slide
- title must already contain the conclusion
- tables only when ranking or comparison matters
- show driver amounts for bridges, not just rate changes
- reference chart assets explicitly when they exist
- do not consider the deck complete if only two bridge charts were produced
- use compact, dashboard-like layouts instead of long spreadsheet screenshots whenever possible
- use traffic-light styling to expose off-budget and worsening indicators
- use waterfall charts for overall profit-factor explanation rather than plain bars
- for category trends, generate charts for the top 10 current-month categories by GMV, but only place 1-3 selected charts into the deck
- each category trend chart must be a single dual-axis chart: GMV as bars, gross margin as a line

## Outline-first rule

The final writing order should be:

1. `report_outline.md`
2. `management_report.md`
3. `ppt_outline.md`
4. `ppt_page_notes.md`

Do not skip directly to the full report.

## Management summary format

Every final deck should answer:

- How far are we from budget?
- Is the problem scale or unit economics?
- Which structures are hurting profit?
- Which products need immediate action?
- Which issues are proven, and which need department explanation?

## Department follow-up page

Close with a page called `待业务解释事项` or similar. Group questions by owner:

- channel / platform operations
- supply chain / logistics
- product / merchandising
- customer service / quality

Each item should point to one observed problem category, not a vague request.
