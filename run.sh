#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
echo "== Compile frontend =="; (cd frontend && node build.mjs)
echo "== Compile backend ==";  python3 -m py_compile backend/app.py backend/data.py && echo "py_compile OK"
echo "== Backend tests ==";    python3 tests/test_backend.py
echo "== Serving on http://localhost:8000 =="; cd backend && PORT=8000 python3 app.py
