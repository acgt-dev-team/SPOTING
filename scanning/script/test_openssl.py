from common.windows_utils import get_imported_functions
from common.crypto_api_rules import CRYPTO_API_RULES
from common.crypto_detection import detect_crypto

binary = r"C:\Program Files\Git\usr\bin\openssl.exe"

print("=" * 60)
print("OpenSSL API Rules")
print("=" * 60)
print(f"Loaded rules: {len(CRYPTO_API_RULES)}")

print("\n" + "=" * 60)
print("Imported APIs")
print("=" * 60)

apis = get_imported_functions(binary)

print(f"Imported functions: {len(apis)}")

matches = []

for api in apis:
    if api in CRYPTO_API_RULES:
        matches.append(api)

print(f"Matched APIs: {len(matches)}\n")

for api in sorted(matches):
    print(api)

print("\n" + "=" * 60)
print("Crypto Detection")
print("=" * 60)

hits = detect_crypto(binary)

print(f"Found {len(hits)} detections\n")

for hit in hits:
    print(hit)