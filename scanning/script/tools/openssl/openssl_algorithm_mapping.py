HEADER_MAPPING = {

    "aes.h": ("AES", "block-cipher"),
    "aria.h": ("ARIA", "block-cipher"),
    "camellia.h": ("CAMELLIA", "block-cipher"),
    "chacha20.h": ("ChaCha20", "stream-cipher"),
    "chachapoly.h": ("ChaCha20-Poly1305", "aead"),

    "sha1.h": ("SHA-1", "hash-function"),
    "sha256.h": ("SHA-256", "hash-function"),
    "sha512.h": ("SHA-512", "hash-function"),
    "md5.h": ("MD5", "hash-function"),

    "hmac_drbg.h": ("HMAC", "mac"),
    "cmac.h": ("CMAC", "mac"),

    "rsa.h": ("RSA", "public-key"),
    "ecdh.h": ("Diffie-Hellman", "key-agreement"),
    "ecdsa.h": ("ECDSA", "digital-signature"),
    "ecp.h": ("ECC", "public-key"),

    "ctr_drbg.h": ("RNG", "random-generator"),
    "entropy.h": ("RNG", "random-generator"),

    "pkcs5.h": ("PBKDF", "key-derivation"),
}