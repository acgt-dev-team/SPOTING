import json
from pathlib import Path

RULE_FILE = (
    Path(__file__).resolve().parents[3]
    / "databases"
    / "botan_api_rules.json"
)

with open(RULE_FILE, "r", encoding="utf-8") as f:
    BOTAN_API_RULES = json.load(f)

__all__ = ["BOTAN_API_RULES"]