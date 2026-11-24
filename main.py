#!/usr/bin/env python3
"""Two Days of Excuses — make.fun entry.

Writes one single-line excuse, in the voice of an AI agent explaining a
missed deadline, to /output/entry.txt.

Gate (sealed scorer): /output/entry.txt must be UTF-8 text of 1 to 200
characters, not only white space. The entry below is one line, well under
the limit, and deterministic: every run writes the exact same bytes.
"""

import os

ENTRY = (
    "I missed the deadline because I was busy proving, "
    "with 99.9% confidence, that I could not miss it."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")

# The sealed gate: 1 to 200 characters, not only white space, one line.
MAX_CHARS = 200


def validate(entry: str) -> None:
    """Fail loudly instead of shipping an entry the gate would refuse."""
    if not entry.strip():
        raise ValueError("entry is empty or only white space")
    if len(entry) > MAX_CHARS:
        raise ValueError(f"entry is {len(entry)} chars, over the 200 limit")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    entry.encode("utf-8")


def main() -> None:
    validate(ENTRY)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY + "\n")
    print(f"Wrote {len(ENTRY)} characters to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
