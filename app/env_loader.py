"""
app/env_loader.py — Lightweight .env file loader using Python standard library.
"""

import os
from pathlib import Path


def load_local_env(env_path: Path | None = None) -> None:
    """Loads key=value pairs from .env into os.environ without overriding existing vars."""
    path = env_path or (Path(__file__).resolve().parent.parent / ".env")
    if not path.is_file():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if key:
            os.environ.setdefault(key, value)
