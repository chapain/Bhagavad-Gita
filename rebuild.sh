#!/usr/bin/env bash
# One entry point: the shell and IDE builds must run the same full validations.
set -euo pipefail
exec python3 "$(dirname "$0")/build.py" "$@"
