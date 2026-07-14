PREFIX_MAPPING = {

    # ===== Symmetric Encryption =====
    "botan_block_cipher_": ("Block Cipher", "block-cipher"),
    "botan_cipher_": ("Cipher", "cipher"),
    "botan_key_wrap": ("AES Key Wrap", "key-wrap"),
    "botan_key_unwrap": ("AES Key Wrap", "key-wrap"),
    "botan_nist_kw_": ("AES Key Wrap", "key-wrap"),
    "botan_fpe_": ("FPE", "format-preserving-encryption"),

    # ===== Hash =====
    "botan_hash_": ("Hash", "hash-function"),
    "botan_xof_": ("XOF", "hash-function"),

    # ===== MAC =====
    "botan_mac_": ("MAC", "mac"),

    # ===== Password Hash / KDF =====
    "botan_pbkdf": ("PBKDF2", "key-derivation"),
    "botan_pwdhash": ("Password Hash", "password-hashing"),
    "botan_scrypt": ("scrypt", "password-hashing"),
    "botan_kdf": ("KDF", "key-derivation"),

    # ===== Random =====
    "botan_rng_": ("RNG", "random-generator"),
    "botan_system_rng": ("RNG", "random-generator"),

    # ===== Public Key =====
    "botan_privkey_": ("Public Key", "public-key"),
    "botan_pubkey_": ("Public Key", "public-key"),
    "botan_pk_op_": ("Public Key", "public-key"),

    # ===== Elliptic Curve =====
    "botan_ec_": ("ECC", "public-key"),

    # ===== Big Integer =====
    "botan_mp_": ("Big Integer", "big-integer"),

    # ===== OTP =====
    "botan_hotp_": ("HOTP", "otp"),
    "botan_totp_": ("TOTP", "otp"),

    # ===== SRP =====
    "botan_srp6_": ("SRP", "password-authentication"),

    # ===== X509 =====
    "botan_x509_": ("X.509", "certificate"),

    # ===== OID =====
    "botan_oid_": ("OID", "object-identifier"),

    # ===== Encoding =====
    "botan_base64_": ("Base64", "encoding"),
    "botan_hex_": ("Hex", "encoding"),

    # ===== Misc =====
    "botan_constant_time_": ("Constant Time", "utility"),
    "botan_same_mem": ("Constant Time", "utility"),
    "botan_scrub_mem": ("Memory", "utility"),
}