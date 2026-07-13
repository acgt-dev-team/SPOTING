import json
from pathlib import Path
from libsodium_algorithm_mapping import HEADER_MAPPING

DATABASE = Path(
    r"C:\AGCT\SPOTING\scanning\databases\libsodium_clean.json"
)

with open(DATABASE, "r") as f:
    api_database = json.load(f)



rules = {}

for header, apis in api_database.items():

    for api in apis:
        
        algorithm, primitive = HEADER_MAPPING.get(
            header,
            ("Unknown", "unknown")
        )

        rules[api] = {
            "library": "Libsodium",
            "header": header,
            "category": "API",
            "algorithm": algorithm,
            "primitive": primitive,

        }

OUTPUT = Path(
    r"C:\AGCT\SPOTING\scanning\databases\libsodium_api_rules.json"
)

with open(OUTPUT, "w") as f:
    json.dump(rules, f, indent=4)

print(f"Generated {len(rules)} rules.")