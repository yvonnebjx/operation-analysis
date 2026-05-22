from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path


ENV_RUN_ROOT = "CBEC_RUN_ROOT"


def runs_base(project_root: Path) -> Path:
    return project_root / "output" / "runs"


def create_timestamped_run_root(project_root: Path) -> Path:
    base = runs_base(project_root)
    base.mkdir(parents=True, exist_ok=True)
    prefix = datetime.now().strftime("%Y%m%d-%H%M%S")
    sequence = 1
    while True:
        candidate = base / f"{prefix}-{sequence:02d}"
        if not candidate.exists():
            candidate.mkdir(parents=True, exist_ok=False)
            write_run_marker(base, candidate)
            write_run_meta(candidate, created=True)
            return candidate
        sequence += 1


def write_run_marker(base: Path, run_root: Path) -> None:
    (base / "_latest_run.txt").write_text(str(run_root), encoding="utf-8")


def write_run_meta(run_root: Path, created: bool = False) -> None:
    meta_path = run_root / "run_meta.json"
    payload = {
        "run_root": str(run_root),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "created": created,
    }
    if meta_path.exists():
        try:
            current = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            current = {}
        current.update(payload)
        payload = current
    meta_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def resolve_run_root(project_root: Path, run_root_arg: str | None) -> Path:
    candidate = run_root_arg or os.environ.get(ENV_RUN_ROOT)
    if candidate:
        run_root = Path(candidate)
        run_root.mkdir(parents=True, exist_ok=True)
        write_run_marker(runs_base(project_root), run_root)
        write_run_meta(run_root, created=False)
        return run_root
    return create_timestamped_run_root(project_root)


def stage_dir(run_root: Path, stage_name: str) -> Path:
    path = run_root / stage_name
    path.mkdir(parents=True, exist_ok=True)
    return path
