#!/usr/bin/env bash
# rebuild.sh — regenerate the Bhagavad Gita app from source data and verify it.
# Usage:  bash rebuild.sh          (after editing any file in source/)
set -euo pipefail
cd "$(dirname "$0")/source"
echo "--- build ---"
python3 build_gita.py          # writes ../index.html
echo "--- verify ---"
python3 check_padas.py | tail -1
python3 check_site_health.py | tail -2
node ../run_gita_app.js | tail -3
# Live browser tests (rendering, i18n, touch, offline). Skipped automatically if
# playwright isn't installed — run:  pip install playwright
#                                    python3 -m playwright install chromium --with-deps
if python3 -c "import playwright" 2>/dev/null; then
  python3 ../browser_checks.py --serve | tail -3
else
  echo "(browser_checks.py skipped — playwright not installed)"
fi
echo "OK: index.html is fresh — commit and push to publish."

