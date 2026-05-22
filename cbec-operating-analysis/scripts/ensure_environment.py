from __future__ import annotations

import argparse
import contextlib
import io
import importlib
import json
import subprocess
import sys
from pathlib import Path

from run_paths import resolve_run_root, stage_dir


REQUIRED_MODULES = {
    "openpyxl": "Workbook profiling and evidence export",
    "numpy": "Chart rendering dependency",
    "matplotlib": "Chart rendering dependency",
}


def get_version(module_name: str) -> str:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
        module = importlib.import_module(module_name)
    return getattr(module, "__version__", "unknown")


def scan_modules() -> tuple[dict[str, str], dict[str, str]]:
    available: dict[str, str] = {}
    missing: dict[str, str] = {}
    for module_name, purpose in REQUIRED_MODULES.items():
        try:
            available[module_name] = get_version(module_name)
        except Exception:
            missing[module_name] = purpose
    return available, missing


def install_requirements(requirements_path: Path) -> None:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)],
        check=True,
    )


def write_markdown(
    path: Path,
    requirements_path: Path,
    available: dict[str, str],
    missing: dict[str, str],
    install_attempted: bool,
) -> None:
    lines = [
        "# Environment Check",
        "",
        f"- Python: `{sys.executable}`",
        f"- Requirements: `{requirements_path}`",
        f"- Install attempted: `{'yes' if install_attempted else 'no'}`",
        "",
        "## Available modules",
        "",
    ]
    if available:
        for name, version in available.items():
            lines.append(f"- `{name}`: `{version}`")
    else:
        lines.append("- none")
    lines.extend(["", "## Missing modules", ""])
    if missing:
        for name, purpose in missing.items():
            lines.append(f"- `{name}`: {purpose}")
    else:
        lines.append("- none")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    project_root = Path.cwd()
    skill_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Check and optionally install CBEC operating-analysis dependencies.")
    parser.add_argument(
        "--run-root",
        default=None,
        help="Root directory for this analysis run. If omitted, a new timestamped run directory is created under output/runs/.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for environment check outputs. Defaults to <run_root>/run_context/",
    )
    parser.add_argument(
        "--requirements",
        default=str(skill_root / "requirements.txt"),
        help="Requirements file used for dependency installation",
    )
    parser.add_argument(
        "--install-missing",
        action="store_true",
        help="Attempt pip installation when required modules are missing",
    )
    args = parser.parse_args()

    run_root = resolve_run_root(project_root, args.run_root)
    output_dir = Path(args.output_dir) if args.output_dir else stage_dir(run_root, "run_context")
    output_dir.mkdir(parents=True, exist_ok=True)
    requirements_path = Path(args.requirements)

    available, missing = scan_modules()
    install_attempted = False

    if missing and args.install_missing:
        install_attempted = True
        install_requirements(requirements_path)
        available, missing = scan_modules()

    payload = {
        "python": sys.executable,
        "requirements": str(requirements_path),
        "install_attempted": install_attempted,
        "available_modules": available,
        "missing_modules": missing,
    }
    (output_dir / "dependency_status.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_markdown(output_dir / "environment_check.md", requirements_path, available, missing, install_attempted)

    if missing:
        raise SystemExit(
            "Missing required modules: "
            + ", ".join(sorted(missing))
            + ". Re-run with --install-missing or install from requirements.txt."
        )

    print(run_root)


if __name__ == "__main__":
    main()
