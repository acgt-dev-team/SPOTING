import json
from pathlib import Path

RULE_FILE = (
    Path(__file__).resolve().parents[3]
    / "databases"
    / "libsodium_api_rules.json"
)

with open(RULE_FILE, "r", encoding="utf-8") as f:
    LIBSODIUM_API_RULES = json.load(f)

__all__ = ["LIBSODIUM_API_RULES"]