import json
from pathlib import Path

RULE_FILE = (
    Path(__file__).resolve().parents[3]
    / "databases"
    / "wolfssl_api_rules.json"
)


print(RULE_FILE)

with open(RULE_FILE, "r", encoding="utf-8") as f:
    WOLFSSL_API_RULES = json.load(f)

__all__ = ["WOLFSSL_API_RULES"]