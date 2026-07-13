import json
from pathlib import Path


INPUT_FILE = Path("mbedtls_api_database.json")
OUTPUT_FILE = Path("mbedtls_clean.json")
SKIP_HEADERS = {
    "async.h",
    "bio.h",
    "conf.h",
    "comp.h",
    "decoder.h",
    "encoder.h",
    "engine.h",
    "err.h",
    "http.h",
    "objects.h",
    "ocsp.h",
    "params.h",
    "property.h",
    "provider.h",
    "store.h",
    "trace.h",
    "txt_db.h",
}

KEEP_PREFIXES = (
    "AES_",
    "BF_",
    "CAST_",
    "Camellia_",
    "DES_",
    "EVP_",
    "HMAC_",
    "MD4_",
    "MD5_",
    "RIPEMD",
    "SHA",
    "SHA1_",
    "SHA224_",
    "SHA256_",
    "SHA384_",
    "SHA512_",
    "RAND_",
    "RSA_",
    "DSA_",
    "DH_",
    "EC_",
    "ECDH_",
    "ECDSA_",
    "EVP_PKEY_",
    "PKCS5_",
    "PKCS12_",
    "CMAC_",
    "HKDF_",
    "mbedtls_",
)

REMOVE_PREFIXES = (
    "ASYNC_",
    "BIO_",
    "BN_",
    "CONF_",
    "ERR_",
    "LHASH_",
    "OBJ_",
    "OPENSSL_",
    "OSSL_",
    "PEM_",
    "UI_",
    "X509_",
    "TS_",
    "TXT_DB_",
    "MBEDTLS_",
)

REMOVE_CONTAINS = (
    "_free",
    "_up_ref",
    "_get0_",
    "_get1_",
    "_get_",
    "_set0_",
    "_set1_",
    "_set_",
    "_copy",
    "_reset",
    "_cleanup",
    "_meth_",
    "_print",
    "_print_fp",
    "_is_a",
    "_get_params",
    "_set_params",
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