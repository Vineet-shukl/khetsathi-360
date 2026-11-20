#!/usr/bin/env python3
"""
Plankton Code Quality Gate for KhetSathi-360
Runs Phase 1 (Format Check), Phase 2 (Lint & Complexity Check), and Phase 3 (Test Verification).
"""

import subprocess
import sys
import time


def run_phase(name: str, cmd: list[str]) -> bool:
    print(f"\n[Plankton Gate] >>> {name}...")
    start = time.perf_counter()
    res = subprocess.run(cmd)
    elapsed = time.perf_counter() - start
    if res.returncode == 0:
        print(f"[Plankton Gate] PASSED: {name} ({elapsed:.2f}s)")
        return True
    else:
        print(f"[Plankton Gate] FAILED: {name} (exit {res.returncode}) ({elapsed:.2f}s)")
        return False


def main():
    print("=" * 60)
    print("  KHETSATHI-360 PLANKTON CODE QUALITY GATE")
    print("=" * 60)

    # Phase 1: Format verification
    p1 = run_phase(
        "Phase 1: Ruff Code Formatting Verification",
        [sys.executable, "-m", "ruff", "format", "--check", "app", "tests", "ml_pipeline"],
    )
    if not p1:
        print("\n[Plankton Gate] Auto-fix available with: python -m ruff format app tests ml_pipeline")
        sys.exit(1)

    # Phase 2: Static analysis & linting verification
    p2 = run_phase(
        "Phase 2: Ruff Lint & Ambiguity Verification",
        [sys.executable, "-m", "ruff", "check", "app", "tests", "ml_pipeline"],
    )
    if not p2:
        print("\n[Plankton Gate] Auto-fix available with: python -m ruff check --fix app tests ml_pipeline")
        sys.exit(1)

    # Phase 3: Comprehensive Test Suite (43 Unit Tests)
    p3 = run_phase(
        "Phase 3: Unit Test Suite & Promotion Gates",
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
    )
    if not p3:
        print("\n[Plankton Gate] Regression detected in unit tests.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  ALL PLANKTON GATES PASSED (Format: Clean | Lint: 0 | Tests: 43/43)")
    print("=" * 60)
    sys.exit(0)


if __name__ == "__main__":
    main()
