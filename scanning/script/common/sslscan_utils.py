import json

import re
import subprocess

import xmltodict



# regex for PEM certs
PEM_BLOCK_RE = re.compile(
    r"-----BEGIN CERTIFICATE-----(?:\r?\n|[\s\S]*?)-----END CERTIFICATE-----",
    flags=re.MULTILINE,
)

# regex to find client-ca-like blocks in raw xml (fallback)
CLIENT_CA_RE = re.compile(r"<client[-_]?ca(?:s)?(?:[^>]*)>([\s\S]*?)</client[-_]?ca(?:s)?>", flags=re.IGNORECASE)

def run_sslscan_xml(target: str, timeout: int = 90):
    """Run sslscan with deep flags and return output as string"""
    # deep flags requested by user
    cmd = [
        "sslscan",
        "--xml=-",
        "--show-certificates",
        "--show-cipher-ids",
        target,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return target, proc.stdout, proc.returncode, proc.stderr
    except FileNotFoundError:
        return target, None, None, "sslscan binary not found"
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode("utf-8", "ignore") if isinstance(e.stdout, bytes) else (e.stdout or "")
        return target, out, None, f"timeout after {timeout}s"

def parse_sslscan_xml(xml_text: str):
    """Parse XML to dict safely"""
    if not xml_text:
        return None
    if isinstance(xml_text, bytes):
        xml_text = xml_text.decode("utf-8", errors="ignore")
    try:
        return xmltodict.parse(xml_text)
    except Exception as e:
        return {"_parse_error": str(e)}



def find_pem_blocks_in_text(text):
    """Extract PEM blocks from string"""
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="ignore")
    if not isinstance(text, str):
        return []
    return PEM_BLOCK_RE.findall(text)

def find_certificate_nodes(parsed):
    """Walk parsed XML dict and collect certificate-related nodes"""
    found = []
    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if "certificate" in k.lower():
                    found.append(v)
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)
    walk(parsed)
    return found

def extract_pems_from_cert_node(node):
    """Extract PEMs from dict/list/string"""
    pems = []
    if not node:
        return pems
    if isinstance(node, str):
        pems.extend(find_pem_blocks_in_text(node))
    elif isinstance(node, dict):
        for v in node.values():
            pems.extend(extract_pems_from_cert_node(v))
    elif isinstance(node, list):
        for v in node:
            pems.extend(extract_pems_from_cert_node(v))
    # dedupe
    seen, out = set(), []
    for pem in pems:
        pem = pem.strip()
        if pem not in seen:
            seen.add(pem)
            out.append(pem)
    return out

def extract_certificates_from_parsed(parsed_xml, raw_xml):
    """Combine parsed XML + raw text search"""
    pems = []
    if parsed_xml:
        for node in find_certificate_nodes(parsed_xml):
            pems.extend(extract_pems_from_cert_node(node))
    pems.extend(find_pem_blocks_in_text(raw_xml))
    # dedupe
    seen, out = set(), []
    for pem in pems:
        if pem not in seen:
            seen.add(pem)
            out.append(pem)
    return out


# ------------------ NEW: Cipher & client CA extractors ------------------

def extract_ciphers(parsed_xml):
    """
    Search parsed XML for cipher entries and return list of dicts:
    { "sslversion": "...", "status": "...", "strength": "...", "cipherName": "..." }
    xmltodict represents attributes with '@' prefix, so we look for '@sslversion' etc.
    """
    ciphers = []

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k.lower().startswith("cipher"):
                    # v may be dict or list or string
                    if isinstance(v, list):
                        for item in v:
                            ciphers.extend(parse_cipher_node(item))
                    else:
                        ciphers.extend(parse_cipher_node(v))
                else:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)
    def parse_cipher_node(n):
        out = []
        if isinstance(n, dict):
            # attributes likely under keys prefixed with '@', and name under 'cipherName' or 'name'
            attrs = {}
            for key, val in n.items():
                if key.startswith("@"):
                    attrs[key[1:]] = val
            # cipher name might be nested
            name = None
            if "cipherName" in n:
                name = n.get("cipherName")
                if isinstance(name, dict) and "#text" in name:
                    name = name["#text"]
            elif "name" in n:
                name = n.get("name")
            elif "#text" in n:
                name = n["#text"]
            # Build entries: if name is a list or dict handle accordingly
            if isinstance(name, list):
                for nm in name:
                    out.append({
                        "sslversion": attrs.get("sslversion") or attrs.get("version"),
                        "status": attrs.get("status"),
                        "strength": attrs.get("strength") or attrs.get("bits"),
                        "cipherName": nm
                    })
            else:
                out.append({
                    "sslversion": attrs.get("sslversion") or attrs.get("version"),
                    "status": attrs.get("status"),
                    "strength": attrs.get("strength") or attrs.get("bits"),
                    "cipherName": name
                })
        elif isinstance(n, str):
            out.append({"cipherName": n})
        return out

    walk(parsed_xml)
    # dedupe while preserving order
    seen = set()
    out = []
    for c in ciphers:
        key = (c.get("sslversion"), c.get("status"), c.get("cipherName"), c.get("strength"))
        if key not in seen:
            seen.add(key)
            out.append(c)
    return out

def extract_client_cas(parsed_xml, raw_xml):
    """
    Heuristically extract client CA info. Prefer parsed XML nodes that include 'client' and 'ca'.
    Fallback: regex search on raw XML for <client-ca> blocks.
    """
    cas = []

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                kl = k.lower()
                if "client" in kl and "ca" in kl:
                    # v might be string, list, dict
                    if isinstance(v, str):
                        cas.append(v.strip())
                    elif isinstance(v, list):
                        for it in v:
                            if isinstance(it, str):
                                cas.append(it.strip())
                            else:
                                cas.append(json.dumps(it))
                    else:
                        # dict or complex: try to stringify relevant text children
                        for subk, subv in (v.items() if isinstance(v, dict) else []):
                            if isinstance(subv, str):
                                cas.append(subv.strip())
                            else:
                                cas.append(json.dumps(subv))
                else:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)
    if parsed_xml:
        walk(parsed_xml)

    # fallback: raw XML regex search
    if not cas and raw_xml:
        if isinstance(raw_xml, bytes):
            raw_xml = raw_xml.decode("utf-8", "ignore")
        for m in CLIENT_CA_RE.findall(raw_xml):
            txt = m.strip()
            if txt:
                cas.append(txt)

    # clean and dedupe
    seen = set()
    out = []
    for c in cas:
        s = c.strip()
        if s and s not in seen:
            seen.add(s)
            out.append(s)
    return out
