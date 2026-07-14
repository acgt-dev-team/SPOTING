import json
from pathlib import Path


INPUT_FILE = Path("libgcrypt_api_database.json")
OUTPUT_FILE = Path("libgcrypt_clean.json")
SKIP_HEADERS = set()

KEEP_PREFIXES = (
    "gcry_cipher_",
    "gcry_md_",
    "gcry_mac_",
    "gcry_pk_",
    "gcry_kdf_",
    "gcry_kem_",
    "gcry_random",
    "gcry_create_nonce",
    "gcry_prime_",
    "gcry_mpi_",
    "gcry_sexp_",
    "gcry_ctx_",
    "gcry_check_version",
    "gcry_control",
    "gcry_free",
    "gcry_realloc",
    "gcry_get_config",
    "gcry_error",
    "gcry_str",
)

REMOVE_PREFIXES = (
    "gcry_log_",
    "gcry_set_",
)


REMOVE_CONTAINS = (
    "_debug",
    "_dump",
)

IGNORE_NAMES = {
    "int",
    "void",
    "char",
    "short",
    "long",
    "float",
    "double",
    "unsigned",
    "signed",

    "if",
    "else",
    "while",
    "for",
    "switch",
    "return",

    "defined",
    "sizeof",

    "type",
    "mapped",
    "of",
    "anymore",

    "N",

    "gpg_err_code",
    "gpg_err_source",
}

def keep_api(name: str) -> bool:
    """
    Decide whether a symbol belongs in the crypto API database.
    """
    if name in IGNORE_NAMES:
        return False
    
    if name.isupper():
        return False

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