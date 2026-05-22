from __future__ import annotations

import argparse
import csv
import contextlib
import importlib
import io
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from run_paths import resolve_run_root, stage_dir

METRIC_LABELS = {
    "GMV": "GMV",
    "营业收入": "Revenue",
    "销售毛利": "Gross Profit",
    "毛利率": "GP%",
    "折扣率": "Discount%",
    "退款率": "Refund%",
    "采购费率": "Purchase%",
    "物流费率": "Logistics%",
    "广告费率": "Ads%",
    "平台费率": "Platform%",
}

FACTOR_LABELS = {
    "销售单价/结构": "Price/Mix",
    "销量差异": "Volume",
    "折扣": "Discount",
    "VAT": "VAT",
    "退款": "Refund",
    "采购": "Purchase",
    "头程": "Headship",
    "头程单价(含二程/关税)": "Headship",
    "海外仓": "Overseas WH",
    "广告": "Ads",
    "佣金": "Commission",
    "配送费": "Delivery",
    "仓储费": "Storage",
    "其他平台费用": "Other Fee",
}

CHANNEL_LABELS = {
    "新兴平台": "Emerging",
    "三方平台": "3P",
    "美国线下": "US Offline",
    "日本线下": "JP Offline",
    "合计": "Total",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_float(value: str | None) -> float:
    if value in (None, ""):
        return 0.0
    return float(value)


def to_millions(value: float) -> float:
    return value / 1_000_000


def sanitize_label(value: str, prefix: str, index: int) -> str:
    if not value:
        return f"{prefix} {index + 1}"
    if value in METRIC_LABELS:
        return METRIC_LABELS[value]
    if value in FACTOR_LABELS:
        return FACTOR_LABELS[value]
    if value in CHANNEL_LABELS:
        return CHANNEL_LABELS[value]
    if " / " in value:
        parts = [sanitize_label(part.strip(), prefix, index) for part in value.split(" / ")]
        return " / ".join(parts)
    if all(ord(ch) < 128 for ch in value):
        return value
    return f"{prefix} {index + 1}"


def metric_lookup(rows: list[dict[str, str]], metric_name: str) -> dict[str, str] | None:
    for row in rows:
        if row.get("metric") == metric_name:
            return row
    return None


def slugify_filename(value: str, fallback: str) -> str:
    ascii_text = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-").lower()
    return ascii_text or fallback


def ensure_plotting(requirements_path: Path, install_missing: bool):
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            importlib.import_module("matplotlib")
            importlib.import_module("numpy")
    except Exception:
        if not install_missing:
            raise SystemExit(
                "Missing plotting dependencies. Run ensure_environment.py with --install-missing "
                "or re-run this script with --install-missing."
            )
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)],
            check=True,
        )

    matplotlib = importlib.import_module("matplotlib")
    matplotlib.use("Agg")
    return importlib.import_module("matplotlib.pyplot")


def write_manifest(chart_dir: Path, entries: list[tuple[str, str, str]]) -> None:
    lines = ["# Chart Manifest", ""]
    for title, source, status in entries:
        lines.append(f"- `{title}` | source=`{source}` | status={status}")
    (chart_dir / "chart_manifest.md").write_text("\n".join(lines), encoding="utf-8")


def make_dashboard_cards(plt, source_path: Path, output_path: Path, title: str) -> bool:
    rows = read_rows(source_path)
    gmv = metric_lookup(rows, "GMV")
    gp = metric_lookup(rows, "销售毛利")
    gp_rate = metric_lookup(rows, "毛利率")
    if not all([gmv, gp, gp_rate]):
        return False

    metrics = [
        ("GMV", to_millions(safe_float(gmv["actual_value"])), safe_float(gmv["budget_value"]), safe_float(gmv["last_year_value"]), "usd"),
        ("Gross Profit", to_millions(safe_float(gp["actual_value"])), safe_float(gp["budget_value"]), safe_float(gp["last_year_value"]), "usd"),
        ("GP%", safe_float(gp_rate["actual_value"]) * 100, safe_float(gp_rate["budget_value"]) * 100, safe_float(gp_rate["last_year_value"]) * 100, "rate"),
    ]

    fig, ax = plt.subplots(figsize=(14, 3.8))
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 1)
    ax.axis("off")

    for idx, (label, actual, budget_raw, last_year_raw, kind) in enumerate(metrics):
        x = idx + 0.05
        width = 0.9
        height = 0.88
        rect = plt.matplotlib.patches.FancyBboxPatch(
            (x, 0.06),
            width,
            height,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=0,
            facecolor="#1736b6",
        )
        ax.add_patch(rect)

        if kind == "usd":
            actual_text = f"{actual:.2f}M"
            budget_delta = safe_float((actual * 1_000_000 - budget_raw) / budget_raw) * 100 if budget_raw else 0.0
            yoy_delta = safe_float((actual * 1_000_000 - last_year_raw) / last_year_raw) * 100 if last_year_raw else 0.0
            budget_text = f"{budget_delta:+.1f}%"
            yoy_text = f"{yoy_delta:+.1f}%"
        else:
            actual_text = f"{actual:.2f}%"
            budget_text = f"{(actual - budget_raw):+.1f}pts"
            yoy_text = f"{(actual - last_year_raw):+.1f}pts"

        budget_color = "#ef4444" if budget_text.startswith("-") else "#84cc16"
        yoy_color = "#ef4444" if yoy_text.startswith("-") else "#84cc16"
        budget_arrow = "↓" if budget_text.startswith("-") else "↑"
        yoy_arrow = "↓" if yoy_text.startswith("-") else "↑"

        ax.text(x + 0.08, 0.80, label, fontsize=20, color="white", fontweight="bold", ha="left", va="center")
        ax.text(x + 0.10, 0.58, actual_text, fontsize=34, color="white", fontweight="bold", ha="left", va="center")
        ax.text(x + 0.08, 0.34, "vs Budget", fontsize=16, color="white", ha="left", va="center")
        ax.text(x + 0.58, 0.34, budget_text, fontsize=18, color="white", fontweight="bold", ha="left", va="center")
        ax.text(x + 0.80, 0.34, budget_arrow, fontsize=22, color=budget_color, fontweight="bold", ha="left", va="center")
        ax.text(x + 0.08, 0.18, "vs LY", fontsize=16, color="white", ha="left", va="center")
        ax.text(x + 0.58, 0.18, yoy_text, fontsize=18, color="white", fontweight="bold", ha="left", va="center")
        ax.text(x + 0.80, 0.18, yoy_arrow, fontsize=22, color=yoy_color, fontweight="bold", ha="left", va="center")

    ax.set_title(title, fontsize=16, fontweight="bold", loc="left")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return True


def make_absolute_kpi_chart(plt, source_path: Path, output_path: Path, title: str) -> bool:
    rows = read_rows(source_path)
    metrics = [row for row in rows if row.get("metric") in {"GMV", "营业收入", "销售毛利"}]
    if not metrics:
        return False

    labels = [sanitize_label(row["metric"], "Metric", idx) for idx, row in enumerate(metrics)]
    actual = [to_millions(safe_float(row["actual_value"])) for row in metrics]
    budget = [to_millions(safe_float(row["budget_value"])) for row in metrics]
    last_year = [to_millions(safe_float(row["last_year_value"])) for row in metrics]

    fig, ax = plt.subplots(figsize=(9, 5))
    positions = range(len(labels))
    width = 0.25
    ax.bar([p - width for p in positions], actual, width=width, label="Actual", color="#0f766e")
    ax.bar(list(positions), budget, width=width, label="Budget", color="#94a3b8")
    ax.bar([p + width for p in positions], last_year, width=width, label="Last year", color="#f59e0b")
    ax.set_xticks(list(positions))
    ax.set_xticklabels(labels)
    ax.set_ylabel("USD M")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return True


def make_rate_kpi_chart(plt, source_path: Path, output_path: Path, title: str) -> bool:
    rows = read_rows(source_path)
    metrics = [
        row
        for row in rows
        if row.get("metric") in {"毛利率", "折扣率", "退款率", "采购费率", "物流费率", "广告费率", "平台费率"}
    ]
    if not metrics:
        return False

    labels = [sanitize_label(row["metric"], "Metric", idx) for idx, row in enumerate(metrics)]
    actual = [safe_float(row["actual_value"]) * 100 for row in metrics]
    budget = [safe_float(row["budget_value"]) * 100 for row in metrics]
    last_year = [safe_float(row["last_year_value"]) * 100 for row in metrics]

    fig, ax = plt.subplots(figsize=(11, 5))
    positions = range(len(labels))
    width = 0.25
    ax.bar([p - width for p in positions], actual, width=width, label="Actual", color="#b91c1c")
    ax.bar(list(positions), budget, width=width, label="Budget", color="#94a3b8")
    ax.bar([p + width for p in positions], last_year, width=width, label="Last year", color="#2563eb")
    ax.set_xticks(list(positions))
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylabel("Rate (%)")
    ax.set_title(title)
    ax.legend(ncols=3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return True


def make_profit_bridge_chart(plt, source_path: Path, output_path: Path, title: str) -> bool:
    rows = read_rows(source_path)
    bridge_rows = [row for row in rows if row.get("subdimension") and row.get("subdimension") != "销量差异"]
    bridge_rows.sort(key=lambda row: abs(safe_float(row.get("profit_impact"))), reverse=True)
    bridge_rows = bridge_rows[:10]
    if not bridge_rows:
        return False

    labels = [sanitize_label(row["subdimension"], "Driver", idx) for idx, row in enumerate(bridge_rows)]
    impacts = [to_millions(safe_float(row["profit_impact"])) for row in bridge_rows]
    colors = ["#bf3f3f" if value < 0 else "#2f8f5b" for value in impacts]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh(labels, impacts, color=colors)
    ax.axvline(0, color="#333333", linewidth=1)
    ax.set_xlabel("Profit impact (USD M)")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return True


def make_profit_waterfall_chart(
    plt,
    bridge_path: Path,
    kpi_path: Path,
    output_path: Path,
    title: str,
) -> bool:
    bridge_rows = read_rows(bridge_path)
    kpi_rows = read_rows(kpi_path)
    gp_row = metric_lookup(kpi_rows, "销售毛利")
    if not bridge_rows or gp_row is None:
        return False

    actual_gp = safe_float(gp_row["actual_value"])
    budget_gp = safe_float(gp_row["budget_value"])
    order = [
        "销量差异",
        "销售单价/结构",
        "折扣",
        "退款",
        "采购",
        "头程",
        "海外仓",
        "广告",
        "佣金",
        "配送费",
        "仓储费",
        "其他平台费用",
        "VAT",
    ]
    by_name = {row["subdimension"]: row for row in bridge_rows if row.get("subdimension")}
    ordered_rows = [by_name[name] for name in order if name in by_name]
    if not ordered_rows:
        return False

    labels = ["Budget GP"] + [sanitize_label(row["subdimension"], "Driver", idx) for idx, row in enumerate(ordered_rows)] + ["Actual GP"]
    values = [budget_gp] + [safe_float(row["profit_impact"]) for row in ordered_rows] + [actual_gp]

    bottoms = [0.0]
    heights = [to_millions(budget_gp)]
    cumulative = budget_gp
    for row in ordered_rows:
        impact = safe_float(row["profit_impact"])
        start = min(cumulative, cumulative + impact)
        bottoms.append(to_millions(start))
        heights.append(abs(to_millions(impact)))
        cumulative += impact
    bottoms.append(0.0)
    heights.append(to_millions(actual_gp))

    colors = ["#1736b6"]
    for row in ordered_rows:
        colors.append("#ef4444" if safe_float(row["profit_impact"]) < 0 else "#65a30d")
    colors.append("#1736b6")

    fig = plt.figure(figsize=(13.5, 5.8))
    gs = fig.add_gridspec(1, 2, width_ratios=[3.8, 1.5])
    ax = fig.add_subplot(gs[0, 0])
    ax_tbl = fig.add_subplot(gs[0, 1])

    xpos = list(range(len(labels)))
    ax.bar(xpos, heights, bottom=bottoms, color=colors, edgecolor="white", linewidth=0.8)
    ax.axhline(0, color="#475569", linewidth=0.8)
    ax.set_xticks(xpos)
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylabel("USD M")
    ax.set_title(title, loc="left", fontweight="bold")

    cumulative = budget_gp
    for idx, row in enumerate(ordered_rows, start=1):
        impact = safe_float(row["profit_impact"])
        y = max(cumulative, cumulative + impact) if impact >= 0 else min(cumulative, cumulative + impact)
        ax.text(idx, to_millions(y) + (0.08 if impact >= 0 else -0.18), f"{to_millions(impact):+.2f}", ha="center", va="bottom" if impact >= 0 else "top", fontsize=8)
        cumulative += impact
    ax.text(0, to_millions(budget_gp) + 0.08, f"{to_millions(budget_gp):.2f}", ha="center", va="bottom", fontsize=8)
    ax.text(len(labels) - 1, to_millions(actual_gp) + 0.08, f"{to_millions(actual_gp):.2f}", ha="center", va="bottom", fontsize=8)

    ax_tbl.axis("off")
    top_rows = sorted(ordered_rows, key=lambda row: abs(safe_float(row["profit_impact"])), reverse=True)[:8]
    table_data = [
        [sanitize_label(row["subdimension"], "Driver", idx), f"{to_millions(safe_float(row['profit_impact'])):+.2f}"]
        for idx, row in enumerate(top_rows)
    ]
    tbl = ax_tbl.table(
        cellText=table_data,
        colLabels=["Driver", "Impact"],
        cellLoc="left",
        loc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.35)
    ax_tbl.set_title("Top Drivers", fontweight="bold", pad=10)

    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return True


def make_refund_channel_chart(plt, source_path: Path, output_path: Path, title: str) -> bool:
    rows = read_rows(source_path)
    rows = [row for row in rows if row.get("subdimension")]
    if not rows:
        return False

    labels = [sanitize_label(row["subdimension"], "Channel", idx) for idx, row in enumerate(rows)]
    actual = [safe_float(row["actual_rate"]) * 100 for row in rows]
    last_year = [safe_float(row["last_year_rate"]) * 100 for row in rows]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    positions = range(len(labels))
    width = 0.35
    ax.bar([p - width / 2 for p in positions], actual, width=width, label="Actual", color="#b91c1c")
    ax.bar([p + width / 2 for p in positions], last_year, width=width, label="Last year", color="#2563eb")
    ax.set_xticks(list(positions))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Refund rate (%)")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return True


def make_top_variance_chart(plt, source_path: Path, output_path: Path, title: str) -> bool:
    rows = read_rows(source_path)
    rows = [row for row in rows if row.get("subdimension")]
    rows.sort(key=lambda row: safe_float(row.get("profit_impact")))
    rows = rows[:8]
    if not rows:
        return False

    labels = [sanitize_label(row["subdimension"], "Group", idx) for idx, row in enumerate(rows)]
    impacts = [to_millions(safe_float(row["profit_impact"])) for row in rows]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh(labels, impacts, color="#bf3f3f")
    ax.axvline(0, color="#333333", linewidth=1)
    ax.set_xlabel("Gross profit variance vs budget (USD M)")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return True


def make_loss_models_chart(plt, source_path: Path, output_path: Path, title: str) -> bool:
    rows = read_rows(source_path)
    rows = [row for row in rows if row.get("model")]
    rows.sort(key=lambda row: safe_float(row.get("gross_profit")))
    rows = rows[:10]
    if not rows:
        return False

    labels = [row["model"] for row in rows]
    gross_profit = [to_millions(safe_float(row["gross_profit"])) for row in rows]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh(labels, gross_profit, color="#7c2d12")
    ax.axvline(0, color="#333333", linewidth=1)
    ax.set_xlabel("Gross profit (USD M)")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return True


def make_category_trend_chart(
    plt,
    category: str,
    rows: list[dict[str, str]],
    output_path: Path,
    title: str,
) -> bool:
    if not rows:
        return False

    labels = [row["period"][2:].replace("-", "/") for row in rows]
    gmv = [to_millions(safe_float(row["gmv"])) for row in rows]
    gross_margin = [safe_float(row["gross_margin"]) * 100 for row in rows]

    fig, ax1 = plt.subplots(figsize=(12, 5.2))
    positions = list(range(len(labels)))
    bars = ax1.bar(positions, gmv, width=0.55, color="#5b9bd5", label="GMV")
    ax1.set_ylabel("GMV (USD M)", color="#374151")
    ax1.set_xticks(positions)
    ax1.set_xticklabels(labels)
    ax1.set_title(title, fontweight="bold")
    ax1.grid(axis="y", linestyle="--", alpha=0.25)

    ax2 = ax1.twinx()
    ax2.plot(positions, gross_margin, color="#f97316", linewidth=2.5, marker="o", label="GP%")
    ax2.set_ylabel("Gross Margin (%)", color="#374151")
    ax2.set_ylim(min(0, min(gross_margin) - 2), max(12, max(gross_margin) + 2))

    for idx, margin in enumerate(gross_margin):
        ax2.text(idx, margin + 0.3, f"{margin:.1f}%", color="#b91c1c", ha="center", va="bottom", fontsize=8)

    handles = [bars, ax2.lines[0]]
    ax1.legend(handles, ["GMV", "GP%"], loc="upper center", ncols=2, frameon=False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return True


def generate_category_trend_pack(plt, trend_csv: Path, selection_csv: Path, chart_dir: Path) -> tuple[str, int]:
    trend_rows = read_rows(trend_csv)
    if not trend_rows:
        return "no_data", 0

    by_category: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in trend_rows:
        by_category[row["category"]].append(row)

    for category_rows in by_category.values():
        category_rows.sort(key=lambda row: row["period"])

    trend_dir = chart_dir / "category_trends"
    trend_dir.mkdir(parents=True, exist_ok=True)
    created = 0
    manifest_lines = ["# Category Trend Charts", ""]
    for idx, (category, rows) in enumerate(sorted(by_category.items(), key=lambda item: int(item[1][0]["target_month_rank"]))):
        rank = rows[0]["target_month_rank"]
        slug = slugify_filename(category, f"category-{idx+1:02d}")
        output_path = trend_dir / f"{rank.zfill(2)}-{slug}.png"
        title = f"GMV and Gross Margin Trend | Rank {rank}"
        ok = make_category_trend_chart(plt, category, rows, output_path, title)
        if ok:
            created += 1
            manifest_lines.append(f"- rank=`{rank}` | category=`{category}` | file=`{output_path.name}`")

    selected_lines = ["# Selected Category Trend Charts", ""]
    if selection_csv.exists():
        selection_rows = read_rows(selection_csv)[:3]
        for idx, row in enumerate(selection_rows, start=1):
            slug = slugify_filename(row["category"], f"category-{idx:02d}")
            file_name = f"{str(row['target_month_rank']).zfill(2)}-{slug}.png"
            selected_lines.append(
                f"- `{row['category']}` | anomaly_score=`{float(row['anomaly_score']):.2f}` | reason=`{row['selection_reason']}` | chart=`category_trends/{file_name}`"
            )
    else:
        selected_lines.append("- none")

    (trend_dir / "chart_manifest.md").write_text("\n".join(manifest_lines), encoding="utf-8")
    (trend_dir / "selected_trend_charts.md").write_text("\n".join(selected_lines), encoding="utf-8")
    return "generated" if created else "no_data", created


def main() -> None:
    project_root = Path.cwd()
    skill_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Generate management-review charts from CBEC evidence files.")
    parser.add_argument(
        "--run-root",
        default=None,
        help="Root directory for this analysis run. If omitted, a new timestamped run directory is created under output/runs/.",
    )
    parser.add_argument("--evidence-dir", default=None, help="Evidence directory. Defaults to <run_root>/evidence/")
    parser.add_argument("--chart-dir", default=None, help="Chart output directory. Defaults to <run_root>/charts/")
    parser.add_argument(
        "--requirements",
        default=str(skill_root / "requirements.txt"),
        help="Requirements file used when chart dependencies are missing",
    )
    parser.add_argument(
        "--install-missing",
        action="store_true",
        help="Attempt to install missing plotting dependencies before charting",
    )
    args = parser.parse_args()

    run_root = resolve_run_root(project_root, args.run_root)
    evidence_dir = Path(args.evidence_dir) if args.evidence_dir else stage_dir(run_root, "evidence")
    chart_dir = Path(args.chart_dir) if args.chart_dir else stage_dir(run_root, "charts")
    requirements_path = Path(args.requirements)
    chart_dir.mkdir(parents=True, exist_ok=True)

    plt = ensure_plotting(requirements_path, args.install_missing)

    targets = [
        {
            "id": "dashboard_kpi_mtd",
            "sources": [evidence_dir / "company" / "company_kpi_mtd.csv"],
            "output": chart_dir / "dashboard_kpi_mtd.png",
            "title": "MTD KPI Dashboard",
            "generator": lambda p, src, out, t: make_dashboard_cards(p, src[0], out, t),
        },
        {
            "id": "company_kpi_mtd",
            "sources": [evidence_dir / "company" / "company_kpi_mtd.csv"],
            "output": chart_dir / "company_kpi_mtd.png",
            "title": "MTD absolute KPI comparison",
            "generator": lambda p, src, out, t: make_absolute_kpi_chart(p, src[0], out, t),
        },
        {
            "id": "company_kpi_ytd",
            "sources": [evidence_dir / "company" / "company_kpi_ytd.csv"],
            "output": chart_dir / "company_kpi_ytd.png",
            "title": "YTD absolute KPI comparison",
            "generator": lambda p, src, out, t: make_absolute_kpi_chart(p, src[0], out, t),
        },
        {
            "id": "company_rates_mtd",
            "sources": [evidence_dir / "company" / "company_kpi_mtd.csv"],
            "output": chart_dir / "company_rates_mtd.png",
            "title": "MTD rate KPI comparison",
            "generator": lambda p, src, out, t: make_rate_kpi_chart(p, src[0], out, t),
        },
        {
            "id": "company_rates_ytd",
            "sources": [evidence_dir / "company" / "company_kpi_ytd.csv"],
            "output": chart_dir / "company_rates_ytd.png",
            "title": "YTD rate KPI comparison",
            "generator": lambda p, src, out, t: make_rate_kpi_chart(p, src[0], out, t),
        },
        {
            "id": "profit_waterfall_mtd",
            "sources": [
                evidence_dir / "company" / "company_profit_bridge_mtd.csv",
                evidence_dir / "company" / "company_kpi_mtd.csv",
            ],
            "output": chart_dir / "profit_waterfall_mtd.png",
            "title": "MTD gross profit waterfall",
            "generator": lambda p, src, out, t: make_profit_waterfall_chart(p, src[0], src[1], out, t),
        },
        {
            "id": "profit_waterfall_ytd",
            "sources": [
                evidence_dir / "company" / "company_profit_bridge_ytd.csv",
                evidence_dir / "company" / "company_kpi_ytd.csv",
            ],
            "output": chart_dir / "profit_waterfall_ytd.png",
            "title": "YTD gross profit waterfall",
            "generator": lambda p, src, out, t: make_profit_waterfall_chart(p, src[0], src[1], out, t),
        },
        {
            "id": "profit_bridge_mtd",
            "sources": [evidence_dir / "company" / "company_profit_bridge_mtd.csv"],
            "output": chart_dir / "profit_bridge_mtd.png",
            "title": "MTD profit bridge",
            "generator": lambda p, src, out, t: make_profit_bridge_chart(p, src[0], out, t),
        },
        {
            "id": "profit_bridge_ytd",
            "sources": [evidence_dir / "company" / "company_profit_bridge_ytd.csv"],
            "output": chart_dir / "profit_bridge_ytd.png",
            "title": "YTD profit bridge",
            "generator": lambda p, src, out, t: make_profit_bridge_chart(p, src[0], out, t),
        },
        {
            "id": "refund_by_channel_mtd",
            "sources": [evidence_dir / "refund" / "refund_by_channel_mtd.csv"],
            "output": chart_dir / "refund_by_channel_mtd.png",
            "title": "MTD refund rate by channel",
            "generator": lambda p, src, out, t: make_refund_channel_chart(p, src[0], out, t),
        },
        {
            "id": "channel_region_risk_mtd",
            "sources": [evidence_dir / "structure" / "channel_region_profit_variance_mtd.csv"],
            "output": chart_dir / "channel_region_risk_mtd.png",
            "title": "MTD channel-region gross profit risk",
            "generator": lambda p, src, out, t: make_top_variance_chart(p, src[0], out, t),
        },
        {
            "id": "category_channel_risk_mtd",
            "sources": [evidence_dir / "structure" / "category_channel_profit_variance_mtd.csv"],
            "output": chart_dir / "category_channel_risk_mtd.png",
            "title": "MTD category-channel gross profit risk",
            "generator": lambda p, src, out, t: make_top_variance_chart(p, src[0], out, t),
        },
        {
            "id": "loss_models_mtd",
            "sources": [evidence_dir / "model" / "loss_models_mtd.csv"],
            "output": chart_dir / "loss_models_mtd.png",
            "title": "MTD negative gross-profit models",
            "generator": lambda p, src, out, t: make_loss_models_chart(p, src[0], out, t),
        },
    ]

    entries: list[tuple[str, str, str]] = []
    for target in targets:
        missing_sources = [source for source in target["sources"] if not source.exists()]
        source_text = ", ".join(str(source) for source in target["sources"])
        if missing_sources:
            entries.append((target["id"], source_text, "missing_source"))
            continue
        created = target["generator"](plt, target["sources"], target["output"], target["title"])
        entries.append((target["id"], source_text, "generated" if created else "no_data"))

    trend_csv = evidence_dir / "structure" / "category_monthly_trend_top10.csv"
    selection_csv = evidence_dir / "structure" / "category_monthly_trend_selection.csv"
    trend_source_text = ", ".join(str(path) for path in [trend_csv, selection_csv])
    if trend_csv.exists():
        status, count = generate_category_trend_pack(plt, trend_csv, selection_csv, chart_dir)
        entries.append(("category_trend_top10", trend_source_text, f"{status}:{count}"))
    else:
        entries.append(("category_trend_top10", trend_source_text, "missing_source"))

    write_manifest(chart_dir, entries)
    print(run_root)


if __name__ == "__main__":
    main()
