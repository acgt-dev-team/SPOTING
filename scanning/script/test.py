from common.crypto_detection import detect_crypto

binary = r"C:\Users\Admin\Downloads\wolfssl-master\wolfssl-master\build\wolfcrypt\test\Release\testwolfcrypt.exe"

hits = detect_crypto(binary)

print("Detected Algorithms:", len(hits))

for hit in hits:
    print(hit)