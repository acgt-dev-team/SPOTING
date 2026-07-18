import json
from pathlib import Path
from libgcrypt_api_mapping import API_PREFIX_MAPPING

DATABASE = Path(
    r"C:\AGCT\SPOTING\scanning\databases\libgcrypt_clean.json"
)

with open(DATABASE, "r") as f:
    api_database = json.load(f)



rules = {}

for header, apis in api_database.items():

    for api in apis:
        
        algorithm = "Unknown"
        primitive = "unknown"

        for prefix, values in API_PREFIX_MAPPING.items():
            if api.startswith(prefix):
                algorithm, primitive = values
                break

        rules[api] = {
            "library": "libgcrypt",
            "header": header,
            "category": "API",
            "algorithm": algorithm,
            "primitive": primitive,

        }

OUTPUT = Path(
    r"C:\AGCT\SPOTING\scanning\databases\libgcrypt_api_rules.json"
)

with open(OUTPUT, "w") as f:
    json.dump(rules, f, indent=4)

print(f"Generated {len(rules)} rules.")