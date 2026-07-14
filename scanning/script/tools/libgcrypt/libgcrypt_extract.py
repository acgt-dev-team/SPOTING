from pathlib import Path
import re
import json

def find_header_files(header_directory: Path):
    """
    Recursively locate every .h file.
    """
    return sorted(header_directory.rglob("*.h"))


def read_header_file(header_path: Path):
    """
    Read the entire header file as a single string.
    """
    with open(header_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()

def is_candidate_function(line: str) -> bool:
    """
    Returns True only for public wolfSSL API declarations.
    """

    line = line.strip()

    if not line:
        return False

    if line.startswith("#"):
        return False

    if line.startswith("/*"):
        return False

    if line.startswith("*"):
        return False

    if "typedef" in line:
        return False

    if "(" not in line:
        return False

    if "defined(" in line:
        return False
    
    if ";" not in line and line.rstrip().endswith("(") is False:
        return False

    return True

def extract_function_name(line: str):
    """
    Extract the function name from a C function declaration.

    Example:

        WOLFSSL_API int wc_AesSetKey(...)
                        ↓
                 wc_AesSetKey
    """

    match = re.search(
        r"""
        \b
        (?:void|int|char|short|long|float|double|
            unsigned|signed|
            word16|word32|word64|
            byte|
            size_t|
            [A-Za-z_][A-Za-z0-9_]*\s*\*)     # pointer return types
        [\s\*]+
        ([A-Za-z_][A-Za-z0-9_]*)
        \s*\(
        """,
        line,
        re.VERBOSE,
    )

    if match:
        return match.group(1)

    return None


def is_public_api(name: str) -> bool:
    return name is not None

def main():
    header_files = [
        Path(r"C:\AGCT\library-sources\libgcrypt-1.12.2\src\gcrypt.h.in")
    ]

    

    print(f"Found {len(header_files)} header files\n")

    api_database = {}

    for header in header_files:

        content = read_header_file(header)

        # Join wrapped declarations
        content = re.sub(r"\\\n", "", content)
        content = re.sub(r"\n\s+", " ", content)

        matches = re.findall(
            r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\([^;{}]*\)\s*;',
            content
        )

        if not matches:
            continue

        header_name = header.name

        if header_name not in api_database:
            api_database[header_name] = set()

        for name in matches:
            api_database[header_name].add(name)

    total = 0

    for header_name in sorted(api_database):

        print("\n" + "=" * 60)
        print(header_name)
        print("=" * 60)

        for api in sorted(api_database[header_name]):
            print(api)
            total += 1

    print(f"\nTotal APIs: {total}")

    export_data = {}

    for header_name in sorted(api_database):
        export_data[header_name] = sorted(api_database[header_name])

    with open("libgcrypt_api_database.json", "w", encoding="utf-8") as file:
        json.dump(export_data, file, indent=4)

    print("\nJSON exported to libgcrypt_api_database.json")


if __name__ == "__main__":
    main()