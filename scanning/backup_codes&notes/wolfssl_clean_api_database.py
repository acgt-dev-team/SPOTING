import json
from pathlib import Path


INPUT_FILE = Path("wolfssl_api_database.json")
OUTPUT_FILE = Path("wolfssl_clean.json")
SKIP_HEADERS = {
    # Existing
    "logging.h",
    "async.h",
    "memory.h",
    "wc_port.h",
    "cpuid.h",
    "quickassist_mem.h",

    # Add these
    "atmel.h",
    "cavium_octeon_sync.h",
    "quickassist_sync.h",
    "renesas_sync.h",
    "renesas-tsip-crypt.h",
    "se050_port.h",
    "wolfcaam.h",
    "wolfcaam_seco.h",
    "iotsafe.h",
    "pkcs12.h",
    "pkcs7.h",
    "tsp.h",
    "wc_lms.h",
    "wc_xmss.h",
    "wc_mldsa.h",
    "wc_mlkem.h",
    "wc_slhdsa.h",
    "cryptocb.h",
    "error-crypt.h",
    "fips_test.h",
    "compress.h",
    "rng_bank.h",
    "kdf.h",
    "wolfmath.h",
    "selftest.h",
    "wc_pkcs11.h",


    
}

KEEP_PREFIXES = (
    "wc_",
    "wolfCrypt_",
    "random.h",
    "puf.h",
    "hpke.h",
    "sakke.h"
)


REMOVE_PREFIXES = (
    "wc_ERR_",
    "wc_debug_",
    "wc_backtrace",
    "wolfSSL_",
    "wolfEvent",
    "wolfAsync",
    "wc_str",
    "wc_Asn1",
    "wc_Cert",
    "wc_Parse",
    "wc_Set",
    "asn_public.h"
)


def keep_api(name: str) -> bool:
    """
    Decide whether a symbol belongs in the crypto API database.
    """

    for prefix in REMOVE_PREFIXES:
        if name.startswith(prefix):
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