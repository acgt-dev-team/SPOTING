from common.crypto_detection import detect_crypto

binary = r"C:\Users\Admin\Downloads\wolfssl-master\wolfssl-master\build\wolfcrypt\test\Release\testwolfcrypt.exe"

results = detect_crypto(binary)

for r in results:
    print(r)