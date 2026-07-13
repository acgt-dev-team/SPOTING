import json
from pathlib import Path


INPUT_FILE = Path("libsodium_api_database.json")
OUTPUT_FILE = Path("libsodium_clean.json")
SKIP_HEADERS = {
}
KEEP_PREFIXES = (
    "crypto_",
    "randombytes_",
    "sodium_",
)

REMOVE_PREFIXES = (
)

REMOVE_CONTAINS = (
    "_free",
    "_cleanup",
)

def keep_api(name: str) -> bool:
    """
    Decide whether a symbol belongs in the crypto API database.
    """

    for prefix in REMOVE_PREFIXES:
        if name.startswith(prefix):
            return False

    for substring in REMOVE_CONTAINS:
        if substring in name:
            return False

    for prefix in KEEP_PREFIXES:
        if name.startswith(prefix):
            return True

    return False


with open(INPUT_FILE, "r", encoding="utf-8") as file:
    api_database = json.load(file)


clean_database = {}

for header, functions in api_database.items():

    if header in SKIP_HEADERS:
        continue

    cleaned = []

    for function in functions:

        if keep_api(function):
            cleaned.append(function)

    if cleaned:
        clean_database[header] = cleaned


with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(clean_database, file, indent=4)

print(f"Saved cleaned database to {OUTPUT_FILE}")