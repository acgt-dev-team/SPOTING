"""
Windows CryptoAPI and CNG detection.
"""

WINDOWS_CRYPTO_FUNCTIONS = {

    # -----------------------------
    # AES / Symmetric Encryption
    # -----------------------------
    "BCryptEncrypt": "AES",
    "BCryptDecrypt": "AES",
    "BCryptGenerateSymmetricKey": "AES",
    "BCryptKeyDerivation": "AES",

    # -----------------------------
    # Hashes
    # -----------------------------
    "BCryptCreateHash": "HASH",
    "BCryptHashData": "HASH",
    "BCryptFinishHash": "HASH",

    # -----------------------------
    # Random Number Generator
    # -----------------------------
    "BCryptGenRandom": "RNG",

    # -----------------------------
    # RSA
    # -----------------------------
    "BCryptGenerateKeyPair": "RSA",
    "NCryptEncrypt": "RSA",
    "NCryptDecrypt": "RSA",
    "CryptEncrypt": "RSA",
    "CryptDecrypt": "RSA",

    # -----------------------------
    # ECC
    # -----------------------------
    "BCryptSecretAgreement": "ECDH",

    # -----------------------------
    # Certificates
    # -----------------------------
    "CertOpenStore": "X509",
    "CertOpenSystemStore": "X509",
    "CertVerifyCertificateChainPolicy": "X509",
}

WINDOWS_ALGORITHM_PROVIDERS = {

    "BCRYPT_AES_ALGORITHM": "AES",

    "BCRYPT_DES_ALGORITHM": "DES",

    "BCRYPT_3DES_ALGORITHM": "3DES",

    "BCRYPT_SHA1_ALGORITHM": "SHA1",

    "BCRYPT_SHA256_ALGORITHM": "SHA256",

    "BCRYPT_SHA384_ALGORITHM": "SHA384",

    "BCRYPT_SHA512_ALGORITHM": "SHA512",

    "BCRYPT_MD5_ALGORITHM": "MD5",

    "BCRYPT_RSA_ALGORITHM": "RSA",

    "BCRYPT_ECDSA_P256_ALGORITHM": "ECDSA",

    "BCRYPT_ECDH_P256_ALGORITHM": "ECDH",

}

from common.windows_utils import (
    get_pe_imports,
    get_pe_symbols,
)

def get_windows_crypto_api(binary_path):

    imports = get_pe_imports(binary_path).lower()

    symbols = get_pe_symbols(binary_path).lower()

    output = imports + "\n" + symbols

    findings = []

    for api, algo in WINDOWS_CRYPTO_FUNCTIONS.items():

        if api.lower() in output:

            findings.append({
                "api": api,
                "algorithm": algo,
                "type": "api"
            })

    return findings

def get_windows_algorithm_providers(binary_path):

    imports = get_pe_imports(binary_path).lower()

    symbols = get_pe_symbols(binary_path).lower()

    output = imports + "\n" + symbols

    findings = []

    for provider, algo in WINDOWS_ALGORITHM_PROVIDERS.items():

        if provider.lower() in output:

            findings.append({
                "provider": provider,
                "algorithm": algo,
                "type": "provider"
            })

    return findings