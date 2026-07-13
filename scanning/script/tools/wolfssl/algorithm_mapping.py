HEADER_MAPPING = {

    # ---------- Symmetric ----------
    "aes.h": ("AES", "block-cipher"),
    "des3.h": ("3DES", "block-cipher"),
    "camellia.h": ("CAMELLIA", "block-cipher"),
    "arc4.h": ("ARC4", "stream-cipher"),
    "chacha.h": ("ChaCha20", "stream-cipher"),
    "chacha20_poly1305.h": ("ChaCha20-Poly1305", "aead"),
    "aria-crypt.h": ("ARIA", "block-cipher"),
    "ascon.h": ("ASCON", "aead"),

    # ---------- Hash ----------
    "sha.h": ("SHA-1", "hash-function"),
    "sha256.h": ("SHA-256", "hash-function"),
    "sha3.h": ("SHA-3", "hash-function"),
    "sha512.h": ("SHA-512", "hash-function"),
    "md2.h": ("MD2", "hash-function"),
    "md4.h": ("MD4", "hash-function"),
    "md5.h": ("MD5", "hash-function"),
    "blake2.h": ("BLAKE2", "hash-function"),
    "ripemd.h": ("RIPEMD", "hash-function"),

    # ---------- MAC ----------
    "hmac.h": ("HMAC", "mac"),
    "poly1305.h": ("Poly1305", "mac"),

    # ---------- Public Key ----------
    "rsa.h": ("RSA", "public-key"),
    "ecc.h": ("ECC", "public-key"),
    "eccsi.h": ("ECC", "public-key"),
    "dh.h": ("Diffie-Hellman", "key-agreement"),
    "dsa.h": ("DSA", "digital-signature"),
    "signature.h": ("Signature", "digital-signature"),
    "hpke.h": ("HPKE", "key-agreement"),

    # ---------- RNG ----------
    "random.h": ("RNG", "random-generator"),

    # ---------- KDF ----------
    "pwdbased.h": ("PBKDF", "key-derivation"),
    "kdf.h": ("KDF", "key-derivation"),
}