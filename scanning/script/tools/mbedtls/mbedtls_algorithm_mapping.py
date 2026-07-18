HEADER_MAPPING = {

    "aes.h": ("AES", "block-cipher"),
    "aria.h": ("ARIA", "block-cipher"),
    "camellia.h": ("Camellia", "block-cipher"),
    "ccm.h": ("AES-CCM", "aead"),
    "gcm.h": ("AES-GCM", "aead"),
    "cipher.h": ("Multiple", "cipher"),
    "des.h": ("DES/3DES", "block-cipher"),

    "chacha20.h": ("ChaCha20", "stream-cipher"),
    "chachapoly.h": ("ChaCha20-Poly1305", "aead"),
    "poly1305.h": ("Poly1305", "mac"),

    "sha1.h": ("SHA-1", "hash-function"),
    "sha256.h": ("SHA-256", "hash-function"),
    "sha3.h": ("SHA-3", "hash-function"),
    "sha512.h": ("SHA-512", "hash-function"),
    "md5.h": ("MD5", "hash-function"),
    "ripemd160.h": ("RIPEMD-160", "hash-function"),
    "md.h": ("Multiple", "hash-function"),

    "cmac.h": ("CMAC", "mac"),

    "hkdf.h": ("HKDF", "key-derivation"),
    "pkcs5.h": ("PBKDF2", "key-derivation"),

    "ctr_drbg.h": ("CTR-DRBG", "random-generator"),
    "hmac_drbg.h": ("HMAC-DRBG", "random-generator"),
    "entropy.h": ("Entropy", "random-generator"),

    "rsa.h": ("RSA", "public-key"),
    "dhm.h": ("Diffie-Hellman", "key-agreement"),
    "ecdh.h": ("ECDH", "key-agreement"),
    "ecdsa.h": ("ECDSA", "digital-signature"),
    "ecp.h": ("ECC", "public-key"),
    "ecjpake.h": ("ECJPAKE", "key-agreement"),

    "pk.h": ("Public Key", "public-key"),

    "pkcs7.h": ("PKCS7", "encoding"),
    "pem.h": ("PEM", "encoding"),
    "asn1.h": ("ASN.1", "encoding"),
    "asn1write.h": ("ASN.1", "encoding"),
    "x509.h": ("X.509", "certificate"),
    "x509_crt.h": ("X.509", "certificate"),
    "x509_csr.h": ("X.509 CSR", "certificate"),

    "ssl.h": ("TLS/SSL", "protocol")
}