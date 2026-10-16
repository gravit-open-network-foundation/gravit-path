# Gravit Path

A verified route from who you are to what you are legally allowed to do, today.

- `CANON.md`: what Gravit Path is, its six principles and its legal guardrails.
- `rules/`: rule packs with a dated official source for every rule (United Kingdom, Switzerland).
- `tools/check_rules.py`: refuses a verified rule without an official source and writes `rules/MANIFEST.json` (SHA-256 of each pack).

```bash
pip install pyyaml pytest && python tools/check_rules.py && pytest -q
```

Status: v0.1 draft, 16 October 2026. Not legal advice. Gravit Open Network Foundation, Apache-2.0.

- `site/`: the website, built with `python tools/build_site.py` (the rules page is generated from the rule packs; CI fails if the site is out of date).
- `qa/cases.yaml`: behaviour tests for the assistant.
