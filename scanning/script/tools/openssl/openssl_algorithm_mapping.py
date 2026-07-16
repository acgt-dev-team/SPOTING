HEADER_MAPPING = {

    # Block ciphers
    "aes.h": ("AES", "block-cipher"),
    "blowfish.h": ("Blowfish", "block-cipher"),
    "camellia.h": ("Camellia", "block-cipher"),
    "cast.h": ("CAST", "block-cipher"),
    "des.h": ("DES/3DES", "block-cipher"),

    # Public key
    "rsa.h": ("RSA", "public-key"),
    "dh.h": ("Diffie-Hellman", "key-agreement"),
    "dsa.h": ("DSA", "digital-signature"),
    "ec.h": ("ECC", "public-key"),

    # Hash
    "sha.h": ("SHA", "hash-function"),
    "md4.h": ("MD4", "hash-function"),
    "md5.h": ("MD5", "hash-function"),
    "ripemd.h": ("RIPEMD-160", "hash-function"),

    # MAC
    "hmac.h": ("HMAC", "mac"),
    "cmac.h": ("CMAC", "mac"),

    # KDF
    "kdf.h": ("KDF", "key-derivation"),

    # RNG
    "rand.h": ("RNG", "random-generator"),

    # EVP abstraction
    "evp.h": ("Multiple", "multiple")
}