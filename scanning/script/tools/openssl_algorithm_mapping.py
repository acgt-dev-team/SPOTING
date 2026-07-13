HEADER_MAPPING = {

    # ---------- Symmetric ----------
    "aes.h": ("AES", "block-cipher"),
    "des.h": ("3DES", "block-cipher"),
    "blowfish.h": ("Blowfish", "block-cipher"),
    "cast.h": ("CAST5", "block-cipher"),
    "camellia.h": ("Camellia", "block-cipher"),

    # ---------- Hash ----------
    "sha.h": ("SHA", "hash-function"),
    "md4.h": ("MD4", "hash-function"),
    "md5.h": ("MD5", "hash-function"),
    "ripemd.h": ("RIPEMD160", "hash-function"),

    # ---------- MAC ----------
    "hmac.h": ("HMAC", "mac"),
    "cmac.h": ("CMAC", "mac"),

    # ---------- Public Key ----------
    "rsa.h": ("RSA", "public-key"),
    "dsa.h": ("DSA", "digital-signature"),
    "dh.h": ("Diffie-Hellman", "key-agreement"),
    "ec.h": ("ECC", "public-key"),

    # ---------- RNG ----------
    "rand.h": ("RNG", "random-generator"),

    # ---------- KDF ----------
    "kdf.h": ("KDF", "key-derivation"),

    # ---------- Generic EVP ----------
    "evp.h": ("Generic Crypto", "generic")
}