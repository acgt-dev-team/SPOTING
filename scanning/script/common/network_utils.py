
import psutil
import socket
import ssl
import os
import platform



INTERPRETERS = (
    "python",
    "php",
    "node",
    "perl",
    "ruby",
    "bash",
    "sh",
)


OS_TYPE = platform.system().lower()

# ======================================================
# Protocol detection
# ======================================================
def detect_protocol(port):
    return {
        443: "TLS",
        22: "SSH",
        500: "IPsec-IKE",
        4500: "IPsec-NAT-T",
    }.get(port, "UNKNOWN")

# ======================================================
# Identify application + script
# ======================================================
def identify_application(proc):
    exe = ""
    script = ""

    try:
        exe = proc.exe()
        cmd = proc.cmdline()
    except Exception:
        return "", "", ""

    if proc.name().lower().startswith(INTERPRETERS):
        for arg in cmd[1:]:
            if os.path.isfile(arg):
                script = arg
                break

    return proc.name(), exe, script

# ======================================================
# TLS probing
# ======================================================
def parse_cipher(cipher):
    if not cipher:
        return ""

    name, proto, bits = cipher
    return f"{name} ({bits} bits)"

def probe_tls(host, port):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=3) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                return f"{ssock.version()} | {parse_cipher(ssock.cipher())}"
    except Exception:
        return ""

# ======================================================
# IPsec detection (service-based)
# ======================================================
def detect_ipsec_services():
    ipsec_entries = []

    for proc in psutil.process_iter(["pid", "name", "exe"]):
        name = (proc.info["name"] or "").lower()

        if OS_TYPE == "linux":
            if name in ("charon", "pluto", "strongswan"):
                ipsec_entries.append(proc)

        elif OS_TYPE == "windows":
            if name in ("ikeext", "policyagent"):
                ipsec_entries.append(proc)

    return ipsec_entries