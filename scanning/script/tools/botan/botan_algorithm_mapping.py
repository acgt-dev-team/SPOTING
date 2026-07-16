HEADER_MAPPING = {

    # Botan exposes its public API through a single FFI header.
    # The individual API names (e.g., botan_hash_*, botan_rng_*, botan_rsa_*)
    # determine the specific algorithm, not the header itself.

    "ffi.h": ("Multiple", "multiple"),

}