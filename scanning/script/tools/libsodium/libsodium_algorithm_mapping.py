HEADER_MAPPING = {

    # Symmetric ciphers
    "crypto_aead_aes256gcm.h": ("AES-256-GCM", "aead"),
    "crypto_aead_chacha20poly1305.h": ("ChaCha20-Poly1305", "aead"),
    "crypto_aead_xchacha20poly1305.h": ("XChaCha20-Poly1305", "aead"),
    "crypto_secretbox.h": ("XSalsa20-Poly1305", "aead"),
    "crypto_stream_chacha20.h": ("ChaCha20", "stream-cipher"),
    "crypto_stream_salsa20.h": ("Salsa20", "stream-cipher"),
    "crypto_stream_xsalsa20.h": ("XSalsa20", "stream-cipher"),

    # Hash
    "crypto_hash_sha256.h": ("SHA-256", "hash-function"),
    "crypto_hash_sha512.h": ("SHA-512", "hash-function"),
    "crypto_generichash.h": ("BLAKE2b", "hash-function"),
    "crypto_shorthash.h": ("SipHash", "hash-function"),

    # MAC
    "crypto_auth.h": ("HMAC", "mac"),
    "crypto_onetimeauth.h": ("Poly1305", "mac"),

    # Public-key
    "crypto_box.h": ("Curve25519", "public-key"),
    "crypto_kx.h": ("X25519", "key-agreement"),
    "crypto_scalarmult.h": ("Curve25519", "key-agreement"),
    "crypto_sign.h": ("Ed25519", "digital-signature"),

    # Password / KDF
    "crypto_pwhash.h": ("Argon2", "key-derivation"),
    "crypto_kdf.h": ("BLAKE2b", "key-derivation"),

    # Random
    "randombytes.h": ("RNG", "random-generator"),

    # Utilities
    "utils.h": ("Utilities", "utility"),
}