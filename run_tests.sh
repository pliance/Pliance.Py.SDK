#!/usr/bin/env bash
# Runs the test suite and writes JUnit-compatible XML results.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

RESULTS_DIR="test-results"
RESULTS_FILE="$RESULTS_DIR/results.xml"
VENV_DIR=".venv"

mkdir -p "$RESULTS_DIR"

PYTHON=python3

if ! "$PYTHON" -c "import pytest, requests, cryptography, jwt" >/dev/null 2>&1; then
    echo "pytest not available for $PYTHON; trying to install test dependencies..."

    if "$PYTHON" -m pip install --quiet --user --break-system-packages pytest requests cryptography pyjwt \
        >/dev/null 2>&1 && "$PYTHON" -c "import pytest, requests, cryptography, jwt" >/dev/null 2>&1; then
        echo "Installed test dependencies for the current user."
    elif rm -rf "$VENV_DIR" && "$PYTHON" -m venv "$VENV_DIR" >/dev/null 2>&1; then
        PYTHON="$VENV_DIR/bin/python"
        "$PYTHON" -m pip install --quiet --upgrade pip
        "$PYTHON" -m pip install --quiet pytest requests cryptography pyjwt
        echo "Set up a virtualenv in $VENV_DIR."
    else
        # No usable pip, and venv creation failed (commonly because the
        # python3-venv OS package, which provides ensurepip, isn't installed).
        # tests.py only needs unittest + requests/cryptography/jwt, so fall
        # back to running it directly rather than hard-failing on pytest.
        echo "Could not install pytest (no usable pip/venv on this system)." >&2
        echo "To get JUnit XML output, install it manually, e.g.: sudo apt install python3-venv" >&2
        echo "Falling back to running tests.py directly with unittest (no JUnit XML)." >&2
        exec "$PYTHON" tests.py "$@"
    fi
fi

"$PYTHON" -m pytest tests.py --junitxml="$RESULTS_FILE" "$@"

echo "JUnit XML results written to $RESULTS_FILE"
