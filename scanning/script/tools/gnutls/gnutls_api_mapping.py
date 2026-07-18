HEADER_MAPPING = {
    "gnutls.h.in": ("TLS", "tls")
}


HEADER_MAPPING.update({

    # Multi-precision integer arithmetic
    "bignum.h": ("MPI", "big-integer"),

    # Constant-time operations
    "constant_time.h": ("Constant Time", "utility"),

    # Error handling
    "error.h": ("Error Handling", "utility"),

    # LMS (Leighton-Micali Signature)
    "lms.h": ("LMS", "digital-signature"),

    # Memory allocator
    "memory_buffer_alloc.h": ("Memory Allocator", "utility"),

    # Network sockets
    "net_sockets.h": ("Network", "network"),

    # NIST AES Key Wrap
    "nist_kw.h": ("AES Key Wrap", "key-wrap"),

    # Platform abstraction
    "platform.h": ("Platform", "utility"),
    "platform_time.h": ("Time", "utility"),

    # PSA Crypto helpers
    "psa_util.h": ("PSA Crypto", "crypto-api"),

    # TLS session cache
    "ssl_cache.h": ("TLS Session Cache", "protocol"),

    # TLS cipher suite helpers
    "ssl_ciphersuites.h": ("TLS Cipher Suite", "protocol"),

    # DTLS cookies
    "ssl_cookie.h": ("DTLS Cookie", "protocol"),

    # TLS session tickets
    "ssl_ticket.h": ("TLS Session Ticket", "protocol"),
})