from pathlib import Path
import re
import json


def read_header_file(header_path: Path):
    """
    Read the entire header file.
    """
    with open(header_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def main():

    header = Path(
        r"C:\AGCT\library-sources\Botan-3.12.0\src\lib\ffi\ffi.h"
    )

    if not header.exists():
        print(f"Header not found: {header}")
        return

    print(f"Reading: {header.name}\n")

    content = read_header_file(header)

    # Join wrapped declarations
    content = re.sub(r"\\\n", "", content)
    content = re.sub(r"\n\s+", " ", content)

    # Extract only Botan C API functions
    matches = re.findall(
        r"\b(botan_[A-Za-z0-9_]+)\s*\(",
        content
    )

    apis = sorted(set(matches))

    print("=" * 60)
    print("Botan FFI APIs")
    print("=" * 60)

    for api in apis:
        print(api)

    print(f"\nTotal APIs: {len(apis)}")

    export = {
        "ffi.h": apis
    }

    with open("botan_api_database.json", "w", encoding="utf-8") as file:
        json.dump(export, file, indent=4)

    print("\nJSON exported to botan_api_database.json")


if __name__ == "__main__":
    main()








   