#!/usr/bin/env python3
"""Check the rule packs and write rules/MANIFEST.json.

Every rule needs id, form, statement, source and status. A rule marked verified must cite an official
source (government, federal or cantonal authority, or the law text). The manifest lists each pack with
its SHA-256 so that a pack can later be signed and anchored with History Keeper: an answer can then name
exactly which version of the rules it used.
"""
import hashlib
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OFFICIAL = ("gov.uk", "admin.ch", "fedlex.admin.ch", "zh.ch", "be.ch", "sg.ch", "legislation.gov.uk")
STATUSES = {"verified", "secondary", "needs_review"}
REQUIRED = ("id", "form", "statement", "source", "status")


def check():
    errors, packs, ids = [], {}, set()
    for f in sorted((ROOT / "rules").glob("*/*.yaml")):
        rules = yaml.safe_load(f.read_text()) or []
        for r in rules:
            for k in REQUIRED:
                if not r.get(k):
                    errors.append(f"{f.name}: {r.get('id', '?')} lacks {k}")
            if r.get("id") in ids:
                errors.append(f"{f.name}: duplicate id {r['id']}")
            ids.add(r.get("id"))
            if r.get("status") not in STATUSES:
                errors.append(f"{r.get('id')}: unknown status {r.get('status')}")
            host = r.get("source", "").split("/")[2] if r.get("source", "").startswith("http") else ""
            if r.get("status") == "verified" and not any(host == d or host.endswith("." + d) for d in OFFICIAL):
                errors.append(f"{r.get('id')}: verified but source {host} is not official")
        packs[str(f.relative_to(ROOT))] = {"sha256": hashlib.sha256(f.read_bytes()).hexdigest(), "rules": len(rules),
                                            "verified": sum(1 for r in rules if r.get("status") == "verified")}
    return errors, packs


if __name__ == "__main__":
    errors, packs = check()
    for e in errors:
        print("ERROR", e)
    (ROOT / "rules" / "MANIFEST.json").write_text(json.dumps(packs, indent=1, sort_keys=True) + "\n")
    for p, m in packs.items():
        print(f"{p}: {m['rules']} rules, {m['verified']} verified, sha256 {m['sha256'][:16]}")
    sys.exit(1 if errors else 0)
