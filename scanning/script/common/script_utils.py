import re

from pathlib import Path



CRYPTO_PATTERNS = {
    "AES": {
        "primitive": "block cipher",
        "patterns": [
            r"AES\.new",
            r"openssl\s+enc\s+-aes-(128|192|256)",
        ],
    },
    "RSA": {
        "primitive": "public-key",
        "patterns": [
            r"RSA\.generate\((\d+)\)",
            r"openssl\s+genrsa\s+(\d+)",
            r"ssh-keygen\s+-t\s+rsa\s+-b\s+(\d+)",
        ],
    },
    "ECC": {
        "primitive": "public-key",
        "patterns": [
            r"EllipticCurve",
            r"secp256r1",
            r"ed25519",
        ],
    },
    "SHA": {
        "primitive": "hash",
        "patterns": [
            r"hashlib\.sha(1|224|256|384|512)",
            r"openssl\s+dgst\s+-sha(1|256|512)",
        ],
    },
    "HMAC": {
        "primitive": "MAC",
        "patterns": [
            r"hmac\.new",
        ],
    },
}



# =====================================================
# FILE SCANNING
# =====================================================
def scan_file(path):
    try:
        text = Path(path).read_text(errors="ignore")
    except Exception:
        return []

    findings = []

    for algo, meta in CRYPTO_PATTERNS.items():
        for pat in meta["patterns"]:
            for m in re.findall(pat, text, re.IGNORECASE):
                key_size = "unknown"

                if isinstance(m, tuple):
                    for x in m:
                        if x.isdigit():
                            key_size = x
                elif isinstance(m, str) and m.isdigit():
                    key_size = m

                findings.append({
                    "algorithm": algo,
                    "primitive": meta["primitive"],
                    "parameters": {
                        "keyLength": key_size,
                    },
                    "function_pattern": pat,
                    "detection_source": {"script-pattern"},
                    "confidence": "high",
                })

    return findings
