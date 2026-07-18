HEADER_MAPPING = {

    "aes.h": ("AES", "block-cipher"),
    "arc4.h": ("RC4", "stream-cipher"),
    "aria-crypt.h": ("ARIA", "block-cipher"),
    "ascon.h": ("ASCON", "aead"),
    "camellia.h": ("Camellia", "block-cipher"),
    "chacha.h": ("ChaCha20", "stream-cipher"),
    "chacha20_poly1305.h": ("ChaCha20-Poly1305", "aead"),
    "des3.h": ("3DES", "block-cipher"),

    "dh.h": ("Diffie-Hellman", "key-agreement"),
    "dsa.h": ("DSA", "digital-signature"),
    "ecc.h": ("ECC", "public-key"),
    "eccsi.h": ("ECCSI", "digital-signature"),
    "rsa.h": ("RSA", "public-key"),

    "hash.h": ("Multiple", "hash-function"),
    "sha.h": ("SHA-1", "hash-function"),
    "sha256.h": ("SHA-256", "hash-function"),
    "sha3.h": ("SHA-3", "hash-function"),
    "sha512.h": ("SHA-512", "hash-function"),
    "md2.h": ("MD2", "hash-function"),
    "md4.h": ("MD4", "hash-function"),
    "md5.h": ("MD5", "hash-function"),
    "ripemd.h": ("RIPEMD-160", "hash-function"),
    "blake2.h": ("BLAKE2", "hash-function"),

    "hmac.h": ("HMAC", "mac"),
    "poly1305.h": ("Poly1305", "mac"),

    "hpke.h": ("HPKE", "key-encapsulation"),

    "pwdbased.h": ("PBKDF", "key-derivation"),

    "random.h": ("RNG", "random-generator"),

    "signature.h": ("Signature", "digital-signature"),

    "srp.h": ("SRP", "key-agreement"),

    "asn_public.h": ("ASN.1", "encoding"),

    "psa.h": ("PSA Crypto", "crypto-api"),

    "puf.h": ("PUF", "device-security"),

    "sakke.h": ("SAKKE", "key-management"),

    "wc_she.h": ("SHE", "key-management"),

    "wolfentropy.h": ("Entropy", "random-generator")
}