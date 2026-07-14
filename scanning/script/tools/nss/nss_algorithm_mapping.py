HEADER_MAPPING = {
    "pk11pub.h": ("PKCS#11", "cryptographic-api"),
    "pk11pqg.h": ("DSA", "parameter-generation"),
    "pk11sdr.h": ("Password Encryption", "secure-storage"),

    "ssl.h": ("TLS", "tls"),
    "cert.h": ("X.509", "certificate"),
    "certdb.h": ("Certificate Store", "certificate"),

    "cryptohi.h": ("Digital Signature", "digital-signature"),

    "keyhi.h": ("Public Key", "public-key"),

    "sechash.h": ("Hash", "hash-function"),
    "secpkcs5.h": ("PBKDF", "key-derivation"),
    "secpkcs7.h": ("PKCS#7", "cms"),

    "pkcs12.h": ("PKCS#12", "keystore"),
    "ocsp.h": ("OCSP", "certificate-validation"),
    "smime.h": ("S/MIME", "email-security"),

    "secasn1.h": ("ASN.1", "encoding"),
    "secder.h": ("DER", "encoding"),

    "secoid.h": ("OID", "algorithm-identification"),

    "nss.h": ("NSS", "library"),
}