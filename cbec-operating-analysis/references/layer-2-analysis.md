# Layer 2 Analysis

Layer 2 turns evidence into management diagnosis.

## Output files

Recommended files under `output/analysis/`:

- `00_signal_board.md`
- `01_exec_summary.md`
- `02_profit_analysis.md`
- `03_structure_analysis.md`
- `04_refund_analysis.md`
- `05_loss_models.md`
- `06_open_questions.md`

Read the following inputs before writing:

- `output/evidence/workbook/field_mapping_draft.md`
- `output/evidence/validation.md`
- anomaly candidate tables when available
- `output/final/report_outline.md` when expanding the full final report

## Writing rules

### 1. Separate conclusion from explanation

Use three labels internally even if the final report is more concise:

- `已证实结论`
- `经营归因`
- `待业务解释`

### 2. Root causes should stop at management categories

Good:

- discount deepening
- refund deterioration
- advertising overspend
- headship increase
- overseas warehouse increase
- commission deterioration
- delivery fee increase
- storage fee increase
- other platform cost increase
- structure shift
- volume shortfall
- selling price / mix deterioration

Do not overclaim unsupported second-order causes such as:

- misleading product description
- warehouse staffing issue
- poor campaign keyword strategy

Those belong to business follow-up, not evidence-only conclusion.

### 3. Abnormal model diagnosis

For each abnormal model, write:

- dominant driver type: `销量不足主导`, `单位经济恶化主导`, or `共同拖累`
- top 2-3 negative profit drivers by amount
- one supporting sentence: `退款不是主因` or `退款率偏高`

### 4. Structural conclusions

Push beyond ranking tables. State what the tables imply:

- which channel mix shift is hurting margin
- which region mix shift is dragging gross profit contribution
- which category-channel combination is structurally weak

Also surface what is worth discussing in the meeting. Do not write every table row into the report.

### 4A. Signal-board rule

Before writing long prose, first create a short signal board:

- what is clearly off budget
- what is mainly scale
- what is mainly unit economics
- which structures and models deserve final-report space

This keeps the final report from turning into a generic table summary.

### 5. Use evidence thresholds

Avoid noisy conclusions from tiny samples. Default filters:

- category or model profit analysis: GMV >= 0.1M
- refund analysis: GMV >= 0.1M for category-level, no threshold for region within channel if channel is already selected
- abnormal model list: GMV >= 0.05M if gross profit is negative, otherwise GMV >= 0.1M

## Tone

Write as an operating analysis lead, not as a forensic auditor.

Prefer:

- `该型号异常主要由折扣、广告和头程三项拖累`
- `退款不是主因`
- `结构 shift 导致利润弹性弱于收入增速`

Avoid:

- `可能是运营没做好`
- `需要进一步看一下`

If something truly cannot be concluded, say which department should explain it and what evidence is missing.
