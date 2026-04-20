#!/usr/bin/env python3
"""
Version consistency checker — ensures VERSION file matches all version references.

Usage:
    python scripts/check_version_consistency.py

Exit codes:
    0 — All versions consistent
    1 — Version mismatch found

Configurable: Edit the PROJECT_NAME and scan directories below to match your project.
"""

import json
import re
import sys
from pathlib import Path

# ── Project Configuration ──────────────────────────────────────────
# TODO: Replace with your project name
PROJECT_NAME = "MyProject"

# TODO: Configure which directories to scan
PYTHON_SOURCE_DIR = Path(__file__).parent.parent
FRONTEND_DIR = Path(__file__).parent.parent / "web-ui"
README_FILE = Path(__file__).parent.parent / "README.md"
# ── End Configuration ──────────────────────────────────────────────


def main():
    root_dir = Path(__file__).parent.parent

    version_file = root_dir / "VERSION"
    if not version_file.exists():
        print("Error: VERSION file not found.")
        sys.exit(1)

    expected_version = version_file.read_text(encoding="utf-8").strip().lstrip("v")
    print(f"Expected version: {expected_version}")

    errors = []

    # Check Python file headers
    header_pattern = re.compile(
        rf"^(?:#| \*) {re.escape(PROJECT_NAME)}(?:\s*-\s*\w+)?\s+v(\d+\.\d+\.\d+)",
        flags=re.MULTILINE,
    )
    for src_file in PYTHON_SOURCE_DIR.glob("*.py"):
        content = src_file.read_text(encoding="utf-8")
        match = header_pattern.search(content)
        if match and match.group(1) != expected_version:
            errors.append(f"{src_file.name}: expected {expected_version}, found {match.group(1)}")

    # Check Frontend file headers (if exists)
    if FRONTEND_DIR and FRONTEND_DIR.exists():
        frontend_src = FRONTEND_DIR / "src"
        if frontend_src.exists():
            js_pattern = re.compile(
                rf"^// {re.escape(PROJECT_NAME)}\s+v(\d+\.\d+\.\d+)",
                flags=re.MULTILINE,
            )
            for src_file in frontend_src.rglob("*.[jt]s*"):
                content = src_file.read_text(encoding="utf-8")
                match = js_pattern.search(content)
                if match and match.group(1) != expected_version:
                    errors.append(f"{src_file.name}: expected {expected_version}, found {match.group(1)}")

    # Check README.md
    if README_FILE.exists():
        content = README_FILE.read_text(encoding="utf-8")
        readme_pattern = re.compile(rf"# {re.escape(PROJECT_NAME)}.*v(\d+\.\d+\.\d+)")
        match = readme_pattern.search(content)
        if match and match.group(1) != expected_version:
            errors.append(f"README.md: expected {expected_version}, found {match.group(1)}")

    # Check package.json (if exists)
    if FRONTEND_DIR:
        package_json = FRONTEND_DIR / "package.json"
        if package_json.exists():
            with open(package_json, encoding="utf-8") as f:
                data = json.load(f)
                if data.get("version") != expected_version:
                    errors.append(f"package.json: expected {expected_version}, found {data.get('version')}")

    if errors:
        print("Version consistency checks failed:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    print("All version checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
