#!/usr/bin/env bash
# Usage: ./apply.sh /path/to/clean/clone/of/ARGON-HEALTH
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
R="${1:?path to ARGON-HEALTH clone}"; H="$(cd "$(dirname "$0")" && pwd)"
cd "$R"; git checkout -b chore/assurance-kit-p0
mkdir -p docs/assurance docs/governance scripts tests
cp -n "$H"/docs/assurance/* docs/assurance/
cp -n "$H"/docs/governance/CR-ASSURANCE-KIT-ADOPTION.md docs/governance/
cp -n "$H"/scripts/argon_assurance_lint.py scripts/
cp -n "$H"/tests/test_argon_assurance_lint.py tests/
python3 scripts/argon_assurance_lint.py --root .
python3 -m unittest discover -s tests -p "test_argon_assurance_lint.py"
git add -A && git status --short
echo "Review, then: git commit -m 'chore(assurance): propose assurance kit v1.0 (P0, no CI)' && git push -u origin chore/assurance-kit-p0"
