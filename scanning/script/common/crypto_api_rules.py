from .libraries.openssl import OPENSSL_API_RULES
from .libraries.wolfssl import WOLFSSL_API_RULES

from .libraries.botan import BOTAN_API_RULES
from .libraries.mbedtls import MBEDTLS_API_RULES
from .libraries.libsodium import LIBSODIUM_API_RULES
from .libraries.libgcrypt import LIBGCRYPT_API_RULES
from .libraries.gnutls import GNUTLS_API_RULES
from .libraries.nss import NSS_API_RULES


CRYPTO_API_RULES = {
    **OPENSSL_API_RULES,
    **WOLFSSL_API_RULES,
    **BOTAN_API_RULES,
    **MBEDTLS_API_RULES,
    **LIBSODIUM_API_RULES,
    **LIBGCRYPT_API_RULES,
    **GNUTLS_API_RULES,
    **NSS_API_RULES,
}