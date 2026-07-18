import json
from pathlib import Path

RULE_FILE = (
    Path(__file__).resolve().parents[3]
    / "databases"
    / "mbedtls_api_rules.json"
)

with open(RULE_FILE, "r", encoding="utf-8") as f:
    MBEDTLS_API_RULES = json.load(f)

__all__ = ["MBEDTLS_API_RULES"]