import json
from pathlib import Path

RULE_FILE = (
    Path(__file__).resolve().parents[3]
    / "databases"
    / "libgcrypt_api_rules.json"
)

with open(RULE_FILE, "r", encoding="utf-8") as f:
    LIBGCRYPT_API_RULES = json.load(f)

__all__ = ["LIBGCRYPT_API_RULES"]