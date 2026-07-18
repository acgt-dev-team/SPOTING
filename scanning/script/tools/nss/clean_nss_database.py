import json
from pathlib import Path


INPUT_FILE = Path("nss_api_database.json")
OUTPUT_FILE = Path("nss_clean.json")
KEEP_HEADERS = {
    "nss.h",
    "pk11pub.h",
    "cryptohi.h",
    "ssl.h",
    "sslproto.h",
    "cert.h",
    "certdb.h",
    "keyhi.h",
    "secitem.h",
    "secasn1.h",
    "secder.h",
    "sechash.h",
    "secmod.h",
    "secoid.h",
    "secpkcs5.h",
    "secpkcs7.h",
    "secrng.h",
    "pk11pqg.h",
    "pk11sdr.h",
    "pkcs11.h",
    "pkcs11f.h",
    "pkcs11n.h",
    "pkcs11uri.h",
    "pkcs12.h",
    "smime.h",
    "ocsp.h",
}

KEEP_PREFIXES = (
    "NSS_",
    "PK11_",
    "PKCS11_",
    "CERT_",
    "SEC_",
    "SECKEY_",
    "SSL_",
    "TLS_",
    "HASH_",
    "SGN_",
    "VFY_",
    "DSAU_",
    "ECDH_",
    "ECDSA_",
    "KEA_",
    "PK11SDR_",
)

REMOVE_PREFIXES = (
    "sqlite3_",
    "inflate",
    "deflate",
    "gz",
    "Hacl_",
    "FStar_",
    "Vale_",
    "PKIX_",
    "NSSUTIL_",
)

REMOVE_CONTAINS = (
    "_private",
    "_debug",
    "_internal",
    "_helper",
    "_test",
    "_impl",
    "_free",
    "_destroy",
)

REMOVE_EXACT = {
    "SSL_IS_SSL2_CIPHER",
    "SSL_REQUIRE_NEVER",
    "SEC_ASN1_CHOOSER_DECLARE",
}

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

    if name in REMOVE_EXACT:
        return False

    return False


with open(INPUT_FILE, "r", encoding="utf-8") as file:
    api_database = json.load(file)


clean_database = {}

for header, functions in api_database.items():

    if header not in KEEP_HEADERS:
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