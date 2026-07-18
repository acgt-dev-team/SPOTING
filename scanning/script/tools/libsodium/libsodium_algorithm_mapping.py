HEADER_MAPPING = {

    # Core
    "core.h": ("Core", "utility"),

    # AEAD
    "crypto_aead_aegis128l.h": ("AEGIS-128L", "aead"),
    "crypto_aead_aegis256.h": ("AEGIS-256", "aead"),
    "crypto_aead_aes256gcm.h": ("AES-256-GCM", "aead"),
    "crypto_aead_chacha20poly1305.h": ("ChaCha20-Poly1305", "aead"),
    "crypto_aead_xchacha20poly1305.h": ("XChaCha20-Poly1305", "aead"),

    # Authentication
    "crypto_auth.h": ("HMAC-SHA512-256", "mac"),
    "crypto_auth_hmacsha256.h": ("HMAC-SHA256", "mac"),
    "crypto_auth_hmacsha512.h": ("HMAC-SHA512", "mac"),
    "crypto_auth_hmacsha512256.h": ("HMAC-SHA512/256", "mac"),

    # Secretbox
    "crypto_secretbox.h": ("XSalsa20-Poly1305", "aead"),

    # Stream ciphers
    "crypto_stream.h": ("Stream Cipher", "stream-cipher"),
    "crypto_stream_chacha20.h": ("ChaCha20", "stream-cipher"),
    "crypto_stream_salsa20.h": ("Salsa20", "stream-cipher"),
    "crypto_stream_xsalsa20.h": ("XSalsa20", "stream-cipher"),
    "crypto_stream_xchacha20.h": ("XChaCha20", "stream-cipher"),

    # Hashing
    "crypto_hash.h": ("SHA-512", "hash-function"),
    "crypto_hash_sha256.h": ("SHA-256", "hash-function"),
    "crypto_hash_sha512.h": ("SHA-512", "hash-function"),
    "crypto_generichash.h": ("BLAKE2b", "hash-function"),
    "crypto_generichash_blake2b.h": ("BLAKE2b", "hash-function"),
    "crypto_shorthash.h": ("SipHash", "hash-function"),
    "crypto_shorthash_siphash24.h": ("SipHash-2-4", "hash-function"),

    # One-time MAC
    "crypto_onetimeauth.h": ("Poly1305", "mac"),
    "crypto_onetimeauth_poly1305.h": ("Poly1305", "mac"),

    # Public-key encryption
    "crypto_box.h": ("Curve25519", "public-key"),
    "crypto_box_curve25519xchacha20poly1305.h": ("Curve25519/XChaCha20-Poly1305", "public-key"),
    "crypto_box_curve25519xsalsa20poly1305.h": ("Curve25519/XSalsa20-Poly1305", "public-key"),

    # Key exchange
    "crypto_kx.h": ("X25519", "key-agreement"),

    # Scalar multiplication
    "crypto_scalarmult.h": ("Curve25519", "key-agreement"),
    "crypto_scalarmult_curve25519.h": ("Curve25519", "key-agreement"),
    "crypto_scalarmult_ed25519.h": ("Ed25519", "key-agreement"),
    "crypto_core_ed25519.h": ("Ed25519", "public-key"),
    "crypto_core_ristretto255.h": ("Ristretto255", "public-key"),

    # Signatures
    "crypto_sign.h": ("Ed25519", "digital-signature"),
    "crypto_sign_ed25519.h": ("Ed25519", "digital-signature"),

    # Password hashing
    "crypto_pwhash.h": ("Argon2", "key-derivation"),
    "crypto_pwhash_argon2i.h": ("Argon2i", "key-derivation"),
    "crypto_pwhash_argon2id.h": ("Argon2id", "key-derivation"),
    "crypto_pwhash_scryptsalsa208sha256.h": ("scrypt", "key-derivation"),

    # KDF
    "crypto_kdf.h": ("BLAKE2b", "key-derivation"),
    "crypto_kdf_blake2b.h": ("BLAKE2b", "key-derivation"),

    # Key derivation
    "crypto_kdf_hkdf_sha256.h": ("HKDF-SHA256", "key-derivation"),
    "crypto_kdf_hkdf_sha512.h": ("HKDF-SHA512", "key-derivation"),

    # Random
    "randombytes.h": ("RNG", "random-generator"),

    # Secret stream
    "crypto_secretstream_xchacha20poly1305.h": ("XChaCha20-Poly1305", "stream"),

    # Utilities
    "utils.h": ("Utilities", "utility"),
}

HEADER_MAPPING.update({

    # Core primitives
    "crypto_core_hchacha20.h": ("HChaCha20", "core"),
    "crypto_core_hsalsa20.h": ("HSalsa20", "core"),
    "crypto_core_salsa20.h": ("Salsa20 Core", "core"),
    "crypto_core_salsa2012.h": ("Salsa20/12 Core", "core"),
    "crypto_core_salsa208.h": ("Salsa20/8 Core", "core"),
    "crypto_core_keccak1600.h": ("Keccak-1600", "permutation"),

    # IP encryption
    "crypto_ipcrypt.h": ("IPCrypt", "encryption"),

    # Ristretto
    "crypto_scalarmult_ristretto255.h": ("Ristretto255", "key-agreement"),

    # Secretbox variants
    "crypto_secretbox_xchacha20poly1305.h": ("XChaCha20-Poly1305", "aead"),
    "crypto_secretbox_xsalsa20poly1305.h": ("XSalsa20-Poly1305", "aead"),

    # Legacy Ed25519 API
    "crypto_sign_edwards25519sha512batch.h": (
        "Ed25519",
        "digital-signature"
    ),

    # Salsa20 stream variants
    "crypto_stream_salsa2012.h": ("Salsa20/12", "stream-cipher"),
    "crypto_stream_salsa208.h": ("Salsa20/8", "stream-cipher"),

    # Constant-time comparison
    "crypto_verify_16.h": ("Constant-Time Verify", "verification"),
    "crypto_verify_32.h": ("Constant-Time Verify", "verification"),
    "crypto_verify_64.h": ("Constant-Time Verify", "verification"),

    # Extendable-output functions
    "crypto_xof_shake128.h": ("SHAKE128", "xof"),
    "crypto_xof_shake256.h": ("SHAKE256", "xof"),
    "crypto_xof_turboshake128.h": ("TurboSHAKE128", "xof"),
    "crypto_xof_turboshake256.h": ("TurboSHAKE256", "xof"),

    # Runtime CPU feature detection
    "runtime.h": ("Runtime", "utility"),

    # Version information
    "version.h": ("Version", "utility"),
})