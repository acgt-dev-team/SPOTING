import json
from pathlib import Path

RULE_FILE = (
    Path(__file__).resolve().parents[3]
    / "databases"
    / "nss_api_rules.json"
)

with open(RULE_FILE, "r", encoding="utf-8") as f:
    NSS_API_RULES = json.load(f)

__all__ = ["NSS_API_RULES"]