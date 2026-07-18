from common.libraries.openssl import OPENSSL_API_RULES
from common.libraries.wolfssl import WOLFSSL_API_RULES
from common.libraries.mbedtls import MBEDTLS_API_RULES
from common.libraries.gnutls import GNUTLS_API_RULES
from common.libraries.nss import NSS_API_RULES
from common.libraries.libsodium import LIBSODIUM_API_RULES
from common.libraries.botan import BOTAN_API_RULES
from common.libraries.libgcrypt import LIBGCRYPT_API_RULES

from common.crypto_api_rules import CRYPTO_API_RULES

libraries = {
    "OpenSSL": OPENSSL_API_RULES,
    "wolfSSL": WOLFSSL_API_RULES,
    "mbedTLS": MBEDTLS_API_RULES,
    "GnuTLS": GNUTLS_API_RULES,
    "NSS": NSS_API_RULES,
    "libsodium": LIBSODIUM_API_RULES,
    "Botan": BOTAN_API_RULES,
    "libgcrypt": LIBGCRYPT_API_RULES,
}

print("Crypto API Rule Counts")
print("-" * 40)

for name, rules in libraries.items():
    print(f"{name:<12}: {len(rules)}")

print("-" * 40)
print(f"Total       : {len(CRYPTO_API_RULES)}")

assert "SSL_CTX_new" in CRYPTO_API_RULES
assert "wc_AesInit" in CRYPTO_API_RULES

print("\n✓ All checks passed.")