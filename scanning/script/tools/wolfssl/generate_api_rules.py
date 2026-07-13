import json
from pathlib import Path
from scanning.script.tools.wolfssl.algorithm_mapping import HEADER_MAPPING

DATABASE = Path(
    r"C:\AGCT\SPOTING\scanning\databases\wolfssl_clean.json"
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
            "library": "wolfSSL",
            "header": header,
            "category": "API",
            "algorithm": algorithm,
            "primitive": primitive,

        }

OUTPUT = Path(
    r"C:\AGCT\SPOTING\scanning\databases\wolfssl_api_rules.json"
)

with open(OUTPUT, "w") as f:
    json.dump(rules, f, indent=4)

print(f"Generated {len(rules)} rules.")