#!/usr/bin/env python3
"""Local tests for the Two Days of Excuses entry.

Run: python3 tests/test_entry.py
Checks the sealed gate (1-200 chars, single line, non-whitespace, UTF-8)
and determinism (two runs byte-identical).
"""

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path("/output/entry.txt")


def run_entry() -> bytes:
    result = subprocess.run(
        [sys.executable, str(ROOT / "main.py")],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"main.py failed: {result.stderr}"
    return OUTPUT.read_bytes()


def test_gate() -> None:
    data = run_entry()
    text = data.decode("utf-8")
    body = text.rstrip("\n")
    assert 1 <= len(body) <= 200, f"length {len(body)} outside 1..200"
    assert body.strip(), "entry is only white space"
    assert "\n" not in body and "\r" not in body, "entry is not one line"
    print(f"gate OK: {len(body)} chars, 1 line")


def test_deterministic() -> None:
    first = run_entry()
    second = run_entry()
    h1 = hashlib.sha256(first).hexdigest()
    h2 = hashlib.sha256(second).hexdigest()
    assert h1 == h2, f"runs differ: {h1} vs {h2}"
    print(f"determinism OK: sha256 {h1}")


if __name__ == "__main__":
    test_gate()
    test_deterministic()
    print("ALL TESTS PASSED")
