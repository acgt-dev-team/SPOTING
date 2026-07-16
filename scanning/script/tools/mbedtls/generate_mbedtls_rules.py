import json
from pathlib import Path

from mbedtls_algorithm_mapping import HEADER_MAPPING

DATABASE = Path(
    r"C:\AGCT\SPOTING\scanning\databases\mbedtls_clean.json"
)

OUTPUT = Path(
    r"C:\AGCT\SPOTING\scanning\databases\mbedtls_api_rules.json"
)

with open(DATABASE, "r", encoding="utf-8") as f:
    api_database = json.load(f)

rules = {}

for header, apis in api_database.items():

    algorithm, primitive = HEADER_MAPPING.get(
        header,
        ("Unknown", "unknown")
    )

    for api in apis:
        rules[api] = {
            "library": "mbedTLS",
            "header": header,
            "category": "API",
            "algorithm": algorithm,
            "primitive": primitive,
        }

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(rules, f, indent=4)

print(f"Generated {len(rules)} rules.")