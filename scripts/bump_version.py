#!/usr/bin/env python3
"""
Version bumper — updates VERSION file and all version references across the project.

Usage:
    python scripts/bump_version.py <new_version>

Example:
    python scripts/bump_version.py 0.2.0

Configurable: Edit the PROJECT_NAME and VERSION_PATTERNS below to match your project.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

# ── Project Configuration ──────────────────────────────────────────
# TODO: Replace with your project name (used in file header patterns)
PROJECT_NAME = "MyProject"

# TODO: Configure which directories to scan for source files
# Python source files at project root
PYTHON_SOURCE_DIR = Path(__file__).parent.parent

# Frontend source directory (set to None if no frontend)
FRONTEND_DIR = Path(__file__).parent.parent / "web-ui"

# README file
README_FILE = Path(__file__).parent.parent / "README.md"
# ── End Configuration ──────────────────────────────────────────────


def main():
    if len(sys.argv) != 2:
        print("Usage: python bump_version.py <new_version>")
        print("Example: python bump_version.py 0.2.0")
        sys.exit(1)

    new_version = sys.argv[1].lstrip("v")
    print(f"Bumping version to {new_version}...")

    root_dir = Path(__file__).parent.parent

    # 1. Update VERSION file
    version_file = root_dir / "VERSION"
    if version_file.exists():
        version_file.write_text(f"v{new_version}\n", encoding="utf-8")
        print("Updated VERSION")

    # 2. Update Python file headers
    # Pattern matches: # MyProject v0.1.0 or # MyProject - subtitle v0.1.0
    header_pattern = re.compile(
        rf"^((?:#| \*) {re.escape(PROJECT_NAME)}(?:\s*-\s*\w+)?\s+v)\d+\.\d+\.\d+",
        flags=re.MULTILINE,
    )
    count = 0
    for src_file in PYTHON_SOURCE_DIR.glob("*.py"):
        content = src_file.read_text(encoding="utf-8")
        new_content, num = header_pattern.subn(rf"\g<1>{new_version}", content)
        if num > 0:
            src_file.write_text(new_content, encoding="utf-8")
            count += 1
    print(f"Updated {count} Python files")

    # 3. Update Frontend file headers (if frontend directory exists)
    if FRONTEND_DIR and FRONTEND_DIR.exists():
        frontend_src = FRONTEND_DIR / "src"
        if frontend_src.exists():
            js_pattern = re.compile(
                rf"^(// {re.escape(PROJECT_NAME)}\s+v)\d+\.\d+\.\d+",
                flags=re.MULTILINE,
            )
            js_count = 0
            for src_file in frontend_src.rglob("*.[jt]s*"):
                content = src_file.read_text(encoding="utf-8")
                new_content, num = js_pattern.subn(rf"\g<1>{new_version}", content)
                if num > 0:
                    src_file.write_text(new_content, encoding="utf-8")
                    js_count += 1
            print(f"Updated {js_count} Frontend files")

    # 4. Update README.md
    if README_FILE.exists():
        content = README_FILE.read_text(encoding="utf-8")
        # Pattern: title with version like "# MyProject - v0.1.0"
        content = re.sub(
            rf"(# \w+.*v)\d+\.\d+\.\d+",
            rf"\g<1>{new_version}",
            content,
        )
        README_FILE.write_text(content, encoding="utf-8")
        print("Updated README.md")

    # 5. Update frontend package.json (if exists)
    if FRONTEND_DIR:
        package_json = FRONTEND_DIR / "package.json"
        if package_json.exists():
            with open(package_json, encoding="utf-8") as f:
                data = json.load(f)
            if data.get("version") != new_version:
                import os

                subprocess.run(
                    ["npm", "version", new_version, "--no-git-tag-version"],
                    cwd=str(FRONTEND_DIR),
                    check=True,
                    shell=(os.name == "nt"),
                )
                print("Updated package.json")
            else:
                print("package.json already at version " + new_version)

    print("Version bump complete.")


if __name__ == "__main__":
    main()
