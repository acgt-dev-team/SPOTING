import json
from pathlib import Path

RULE_FILE = (
    Path(__file__).resolve().parents[3]
    / "databases"
    / "openssl_api_rules.json"
)


with open(RULE_FILE, "r", encoding="utf-8") as f:
    OPENSSL_API_RULES = json.load(f)

__all__ = ["OPENSSL_API_RULES"]