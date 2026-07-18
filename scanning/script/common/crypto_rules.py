CRYPTO_RULES = {
    # === Symmetric Block Ciphers ===
    "AES": {
        "assetType": "algorithm",
        "algorithmProperties": {
            "primitive": "block-cipher",
            "algorithm": "AES",
            "modes": ["ECB", "CBC", "CTR", "GCM", "CCM", "XTS"],
            "keyLengths": [128, 192, 256]
        }
    },
    "3DES": {
        "assetType": "algorithm",
        "algorithmProperties": {
            "primitive": "block-cipher",
            "algorithm": "3DES",
            "keyLengths": [112, 168]
        }
    },
    "DES": {
        "assetType": "algorithm",
        "algorithmProperties": {
            "primitive": "block-cipher",
            "algorithm": "DES",
            "deprecated": True,
            "keyLengths": [56]
        }
    },
    "Blowfish": {"assetType":"algorithm","algorithmProperties":{"primitive":"block-cipher","algorithm":"Blowfish"}},
    "CAST5": {"assetType":"algorithm","algorithmProperties":{"primitive":"block-cipher","algorithm":"CAST5"}},
    "CAST6": {"assetType":"algorithm","algorithmProperties":{"primitive":"block-cipher","algorithm":"CAST6"}},
    "RC2": {"assetType":"algorithm","algorithmProperties":{"primitive":"block-cipher","algorithm":"RC2"}},
    "RC5": {"assetType":"algorithm","algorithmProperties":{"primitive":"block-cipher","algorithm":"RC5"}},
    "RC6": {"assetType":"algorithm","algorithmProperties":{"primitive":"block-cipher","algorithm":"RC6"}},
    "Twofish": {"assetType":"algorithm","algorithmProperties":{"primitive":"block-cipher","algorithm":"Twofish"}},
    "CAMELLIA": {"assetType":"algorithm","algorithmProperties":{"primitive":"block-cipher","algorithm":"CAMELLIA"}},
    "Serpent": {"assetType":"algorithm","algorithmProperties":{"primitive":"block-cipher","algorithm":"Serpent"}},
    "ARIA": {"assetType":"algorithm","algorithmProperties":{"primitive":"block-cipher","algorithm":"ARIA"}},

    # === Stream Ciphers ===
    "ChaCha": {"assetType":"algorithm","algorithmProperties":{"primitive":"stream-cipher","algorithm":"ChaCha"}},
    "ChaCha20": {"assetType":"algorithm","algorithmProperties":{"primitive":"stream-cipher","algorithm":"ChaCha20"}},
    "Salsa20": {"assetType":"algorithm","algorithmProperties":{"primitive":"stream-cipher","algorithm":"Salsa20"}},
    "RABBIT": {"assetType":"algorithm","algorithmProperties":{"primitive":"stream-cipher","algorithm":"RABBIT"}},
    "3GPP-XOR": {"assetType":"algorithm","algorithmProperties":{"primitive":"stream-cipher","algorithm":"3GPP-XOR"}},
    "A5/1": {"assetType":"algorithm","algorithmProperties":{"primitive":"stream-cipher","algorithm":"A5/1"}},
    "A5/2": {"assetType":"algorithm","algorithmProperties":{"primitive":"stream-cipher","algorithm":"A5/2"}},
    "CMEA": {"assetType":"algorithm","algorithmProperties":{"primitive":"mac","algorithm":"CMEA"}},

    # === AEAD ===
    "AES-GCM": {"assetType":"algorithm","algorithmProperties":{"primitive":"aead","algorithm":"AES","mode":"GCM"}},
    "CHACHA20-POLY1305": {"assetType":"algorithm","algorithmProperties":{"primitive":"aead","algorithm":"ChaCha20","mac":"Poly1305"}},

    # === MAC ===
    "Poly1305": {"assetType":"algorithm","algorithmProperties":{"primitive":"mac","algorithm":"Poly1305"}},
    "CMAC": {"assetType":"algorithm","algorithmProperties":{"primitive":"mac","algorithm":"CMAC"}},
    "HMAC": {"assetType":"algorithm","algorithmProperties":{"primitive":"mac","algorithm":"HMAC","hashFunctions":["SHA-256","SHA-384","SHA-512"]}},

    # === Hash Functions ===
    "SHA-1": {"assetType":"algorithm","algorithmProperties":{"primitive":"hash-function","algorithm":"SHA-1","deprecated":True}},
    "SHA-2": {"assetType":"algorithm","algorithmProperties":{"primitive":"hash-function","algorithm":"SHA-2"}},
    "SHA-3": {"assetType":"algorithm","algorithmProperties":{"primitive":"hash-function","algorithm":"SHA-3"}},
    "SHA-256": {"assetType":"algorithm","algorithmProperties":{"primitive":"hash-function","algorithm":"SHA-256"}},
    "SHA-384": {"assetType":"algorithm","algorithmProperties":{"primitive":"hash-function","algorithm":"SHA-384"}},
    "SHA-512": {"assetType":"algorithm","algorithmProperties":{"primitive":"hash-function","algorithm":"SHA-512"}},
    "MD2": {"assetType":"algorithm","algorithmProperties":{"primitive":"hash-function","algorithm":"MD2"}},
    "MD4": {"assetType":"algorithm","algorithmProperties":{"primitive":"hash-function","algorithm":"MD4"}},
    "MD5": {"assetType":"algorithm","algorithmProperties":{"primitive":"hash-function","algorithm":"MD5","deprecated":True}},
    "BLAKE2": {"assetType":"algorithm","algorithmProperties":{"primitive":"hash-function","algorithm":"BLAKE2"}},
    "BLAKE3": {"assetType":"algorithm","algorithmProperties":{"primitive":"hash-function","algorithm":"BLAKE3"}},
    "RIPEMD": {"assetType":"algorithm","algorithmProperties":{"primitive":"hash-function","algorithm":"RIPEMD"}},
    "bcrypt": {"assetType":"algorithm","algorithmProperties":{"primitive":"hash-function","algorithm":"bcrypt"}},

    # === Public Key / Digital Signature ===
    "RSAES-PKCS1": {"assetType":"algorithm","algorithmProperties":{"primitive":"public-key-encryption","algorithm":"RSA","keyLengths":[1024,2048,3072,4096],"paddings":["PKCS1v1.5"]}},
    "RSAES-OAEP": {"assetType":"algorithm","algorithmProperties":{"primitive":"public-key-encryption","algorithm":"RSA","keyLengths":[1024,2048,3072,4096],"paddings":["OAEP"]}},
    "RSASSA-PKCS1": {"assetType":"algorithm","algorithmProperties":{"primitive":"digital-signature","algorithm":"RSA"}},
    "RSASSA-PSS": {"assetType":"algorithm","algorithmProperties":{"primitive":"digital-signature","algorithm":"RSA","paddings":["PSS"]}},
    "DSA": {"assetType":"algorithm","algorithmProperties":{"primitive":"digital-signature","algorithm":"DSA"}},
    "ECDSA": {"assetType":"algorithm","algorithmProperties":{"primitive":"digital-signature","algorithm":"ECDSA","curves":["P-256","P-384","P-521","secp256k1"],"hashFunctions":["SHA-256","SHA-384","SHA-512"]}},
    "EdDSA": {"assetType":"algorithm","algorithmProperties":{"primitive":"digital-signature","algorithm":"EdDSA"}},
    "ECIES": {"assetType":"algorithm","algorithmProperties":{"primitive":"key-agreement","algorithm":"ECIES"}},
    "ECDH": {"assetType":"algorithm","algorithmProperties":{"primitive":"key-agreement","algorithm":"ECDH","curves":["P-256","P-384","X25519","X448"]}},
    "X3DH": {"assetType":"algorithm","algorithmProperties":{"primitive":"key-agreement","algorithm":"X3DH"}},
    "FFDH": {"assetType":"algorithm","algorithmProperties":{"primitive":"key-agreement","algorithm":"FFDH"}},
    "ElGamal": {"assetType":"algorithm","algorithmProperties":{"primitive":"public-key-encryption","algorithm":"ElGamal"}},
    "BLS": {"assetType":"algorithm","algorithmProperties":{"primitive":"digital-signature","algorithm":"BLS"}},
    "XMSS": {"assetType":"algorithm","algorithmProperties":{"primitive":"digital-signature","algorithm":"XMSS"}},
    "ML-KEM": {"assetType":"algorithm","algorithmProperties":{"primitive":"key-agreement","algorithm":"ML-KEM"}},
    "ML-DSA": {"assetType":"algorithm","algorithmProperties":{"primitive":"digital-signature","algorithm":"ML-DSA"}},

    # === KDF / PRF / RNG ===
    "PBKDF1": {"assetType":"algorithm","algorithmProperties":{"primitive":"key-derivation","algorithm":"PBKDF1"}},
    "PBKDF2": {"assetType":"algorithm","algorithmProperties":{"primitive":"key-derivation","algorithm":"PBKDF2"}},
    "PBES1": {"assetType":"algorithm","algorithmProperties":{"primitive":"key-derivation","algorithm":"PBES1"}},
    "PBES2": {"assetType":"algorithm","algorithmProperties":{"primitive":"key-derivation","algorithm":"PBES2"}},
    "PBMAC1": {"assetType":"algorithm","algorithmProperties":{"primitive":"key-derivation","algorithm":"PBMAC1"}},
    "HKDF": {"assetType":"algorithm","algorithmProperties":{"primitive":"key-derivation","algorithm":"HKDF"}},
    "SP800-108": {"assetType":"algorithm","algorithmProperties":{"primitive":"key-derivation","algorithm":"SP800-108"}},
    "KMAC": {"assetType":"algorithm","algorithmProperties":{"primitive":"key-derivation","algorithm":"KMAC"}},
    "Fortuna": {"assetType":"algorithm","algorithmProperties":{"primitive":"random-generator","algorithm":"Fortuna"}},
    "Yarrow": {"assetType":"algorithm","algorithmProperties":{"primitive":"random-generator","algorithm":"Yarrow"}},
    "TUAK": {"assetType":"algorithm","algorithmProperties":{"primitive":"random-generator","algorithm":"TUAK"}},
    "MILENAGE": {"assetType":"algorithm","algorithmProperties":{"primitive":"key-derivation","algorithm":"MILENAGE"}},

    # === Protocols ===
    "TLS": {"assetType":"protocol","protocolProperties":{"protocolType":"tls","versions":["1.0","1.1","1.2","1.3"]}},
    "SSL": {"assetType":"protocol","protocolProperties":{"protocolType":"ssl","versions":["2.0","3.0"],"deprecated":True}},
    "IPSec": {"assetType": "protocol","protocolProperties": {"protocolType": "ipsec","versions": ["IKEv1", "IKEv2"] }},
    "SSH" : {"assetType": "protocol","protocolProperties": {"protocolType": "ssh","versions": ["1.0", "2.0"], "deprecated": True }},

    # === Others / miscellaneous default entries ===
    "IDEA": {"assetType":"algorithm","algorithmProperties":{"primitive":"block-cipher","algorithm":"IDEA"}},
    "SNOW3G": {"assetType":"algorithm","algorithmProperties":{"primitive":"stream-cipher","algorithm":"SNOW3G"}},
    "Skipjack": {"assetType":"algorithm","algorithmProperties":{"primitive":"block-cipher","algorithm":"Skipjack"}},
    "SEED": {"assetType":"algorithm","algorithmProperties":{"primitive":"block-cipher","algorithm":"SEED"}}
}

CRYPTO_LIB_PATTERNS = [

    # OpenSSL
    "libcrypto",
    "libssl",

    # Windows CryptoAPI
    "bcrypt",
    "crypt32",
    "cryptbase",
    "ncrypt",
    "ncryptprov",
    "rsaenh",
    "dssenh",
    "schannel",

    # Linux libraries
    "gnutls",
    "libgcrypt",
    "libsodium",
    "nettle",
    "mbedtls",
    "wolfssl",
    "boringssl",
    "libmbedcrypto",
    "libmbedtls",
    "libmbedx509",
    "libnss3",
    "libnspr4",
]