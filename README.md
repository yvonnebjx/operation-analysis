# Operation Analysis — Accio Skills

Custom agent skills for business operations analysis, built for [Accio Work](https://www.accio.com/work/doc) AI agents.

A collection of custom skills built for [Accio Work](https://www.accio.com/work/doc) AI agents.

## Skills

### financial-report-visualizer

End-to-end workflow for batch financial data analysis of listed companies: search, verify, compute metrics (margins, YoY growth), classify into sectors, generate analysis reports, and produce publication-quality bubble charts with CJK font support and automatic label repulsion.

- **SKILL.md** — Workflow instructions for the agent
- **scripts/generate_bubble_chart.py** — Canonical bubble chart generation script

### category-management-matrix

Analyze e-commerce management reports (Excel) to perform YTD YoY analysis and categorize product categories into a 4-quadrant management matrix (Stars, Cash Cows, Volume/Question Marks, Dogs).

- **SKILL.md** — Workflow instructions for the agent
- **scripts/analyze_mgmt_report.py** — Excel analysis and chart generation script

## Usage

These skills are designed to be loaded into an Accio Work agent. See [Accio Work documentation](https://www.accio.com/work/doc) for how to install skills.

## Development

When updating a skill, edit the files in this repo directly and push:

```bash
git add -A
git commit -m "description of changes"
git push
```

A `sync.sh` script is also provided to sync the latest versions from an Accio agent-core installation into this repo.
