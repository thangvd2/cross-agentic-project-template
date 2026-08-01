#!/usr/bin/env bash
# Protected Branch Guard — blocks commits AND pushes to master/dev.
# Runs at both pre-commit and pre-push stages (see .pre-commit-config.yaml).
# Human bypass: git commit --no-verify / git push --no-verify
set -euo pipefail

BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [[ "$BRANCH" == "master" || "$BRANCH" == "dev" || "$BRANCH" == "main" ]]; then
  echo "❌ PROTECTED BRANCH: Cannot commit/push directly to '$BRANCH'."
  echo "Create a feature branch first: git checkout -b feature/your-feature dev"
  exit 1
fi
