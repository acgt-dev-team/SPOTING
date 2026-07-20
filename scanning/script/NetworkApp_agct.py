#!/usr/bin/env python3

import os
import psutil

from common.network_utils import (
    detect_protocol,
    identify_application,
    probe_tls,
    detect_ipsec_services,
)

from common.binary_profile import BinaryProfile
from common.csv_exporter import export_csv
from common.json_exporter import export_json


def main():

    profiles = []
    seen = set()

    connections = psutil.net_connections(kind="inet")
    total = len(connections)

    # ======================================================
    # Scan TLS / SSH connections
    # ======================================================
    for index, conn in enumerate(connections, start=1):

        print(f"[{index}/{total}] Processing connection")

        if not conn.pid:
            continue

        key = (conn.pid, conn.raddr)

        if key in seen:
            continue

        seen.add(key)

        try:
            proto = detect_protocol(
                conn.raddr.port if conn.raddr else conn.laddr.port
            )

            if proto not in ("TLS", "SSH"):
                continue

            proc = psutil.Process(conn.pid)

            pname, exe, script = identify_application(proc)

            profile = BinaryProfile(
                path=exe,
                filename=os.path.basename(exe) if exe else pname,
                extension="network",
            )

            crypto = ""

            if proto == "TLS" and conn.raddr:
                crypto = probe_tls(
                    conn.raddr.ip,
                    conn.raddr.port,
                )

            profile.detections = [{
                "type": "network_application",
                "role": "CLIENT" if conn.raddr else "SERVER",
                "protocol": proto,
                "process": pname,
                "pid": conn.pid,
                "script": script,
                "remote_ip": conn.raddr.ip if conn.raddr else "",
                "remote_port": conn.raddr.port if conn.raddr else conn.laddr.port,
                "crypto": crypto,
            }]

            profiles.append(profile)

        except Exception:
            continue

    # ======================================================
    # Scan IPsec services
    # ======================================================
    for proc in detect_ipsec_services():

        try:
            pname, exe, _ = identify_application(proc)

            profile = BinaryProfile(
                path=exe,
                filename=os.path.basename(exe) if exe else pname,
                extension="network",
            )

            profile.detections = [{
                "type": "ipsec_service",
                "protocol": "IPsec",
                "pid": proc.pid,
                "crypto": "IKE / ESP (kernel-managed)",
            }]

            profiles.append(profile)

        except Exception:
            continue

    # ======================================================
    # Export results
    # ======================================================
    export_csv(
        profiles,
        output_file="network_app.csv",
    )

    json_result = export_json(
        profiles,
        output_file="network_app.json",
    )

    return json_result


def run_scan():
    return main()


if __name__ == "__main__":
    main()