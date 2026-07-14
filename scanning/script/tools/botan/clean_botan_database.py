import json
from pathlib import Path

INPUT_FILE = Path("botan_api_database.json")
OUTPUT_FILE = Path("botan_clean.json")

REMOVE = (
    "botan_error_description",
    "botan_error_last_exception_message",
    "botan_version_major",
    "botan_version_minor",
    "botan_version_patch",
    "botan_version_string",
    "botan_version_datestamp",
    "botan_ffi_api_version",
    "botan_ffi_supports_api",
)


def keep_api(name: str) -> bool:
    """
    Decide whether a symbol belongs in the crypto API database.
    """

    for api in REMOVE:
        if name == api:
            return False

    return True


with open(INPUT_FILE, "r", encoding="utf-8") as file:
    api_database = json.load(file)

clean_database = {}

for header, functions in api_database.items():

    cleaned = []

    for function in functions:
        if keep_api(function):
            cleaned.append(function)

    if cleaned:
        clean_database[header] = cleaned

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(clean_database, file, indent=4)

print(f"Saved cleaned database to {OUTPUT_FILE}")