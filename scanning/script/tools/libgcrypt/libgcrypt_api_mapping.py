API_PREFIX_MAPPING = {
    "gcry_cipher_": ("Cipher", "block-cipher"),
    "gcry_md_": ("Hash", "hash-function"),
    "gcry_mac_": ("MAC", "mac"),
    "gcry_pk_": ("Public Key", "public-key"),
    "gcry_kdf_": ("KDF", "key-derivation"),
    "gcry_kem_": ("KEM", "key-encapsulation"),
    "gcry_random": ("RNG", "random-generator"),
    "gcry_create_nonce": ("RNG", "random-generator"),
    "gcry_prime_": ("Prime", "prime-generation"),
    "gcry_mpi_": ("MPI", "big-integer"),
    "gcry_sexp_": ("S-Expression", "key-encoding"),
    "gcry_ctx_": ("Context", "context"),
}