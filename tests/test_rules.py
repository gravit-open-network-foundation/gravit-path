import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
from check_rules import check

def test_rule_packs_are_valid():
    errors, packs = check()
    assert errors == [], errors
    assert packs and all(m["rules"] > 0 for m in packs.values())
