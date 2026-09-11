#!/usr/bin/env python3
"""Check that every inline comment anchor falls inside a diff hunk.

    gh api repos/<owner>/<repo>/pulls/<PR>/files --paginate > files.json
    ./check-anchors.py files.json payload.json

An anchor outside the diff fails the whole POST /reviews call.
"""
import json
import re
import sys


def commentable(patch):
    """Right-side line numbers actually present in the diff."""
    ok, new = set(), None
    for line in patch.split("\n"):
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
        if m:
            new = int(m.group(1))
            continue
        if new is None:
            continue
        if line.startswith(("+", " ")):
            ok.add(new)
            new += 1
    return ok


def main(files_path, payload_path):
    files = {f["filename"]: f.get("patch", "") for f in json.load(open(files_path))}
    payload = json.load(open(payload_path))
    failed = False

    for c in payload.get("comments", []):
        path = c["path"]
        start, end = c.get("start_line", c["line"]), c["line"]
        if path not in files:
            print(f"NOT IN DIFF   {path}:{start}-{end}  (file not in the diff)")
            failed = True
            continue
        ok = commentable(files[path])
        miss = [n for n in range(start, end + 1) if n not in ok]
        if miss:
            print(f"OUTSIDE HUNK  {path}:{start}-{end}  lines: {miss}")
            failed = True
        else:
            print(f"OK            {path}:{start}-{end}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
