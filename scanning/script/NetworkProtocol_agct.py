#!/usr/bin/env python3

import os

from common.binary_inventory import list_tls_targets

from common.sslscan_utils import (
    run_sslscan_xml,
    parse_sslscan_xml,
    extract_ciphers,
    extract_client_cas,
    extract_certificates_from_parsed,
)

from common.binary_profile import BinaryProfile

from common.csv_exporter import export_csv

from common.json_exporter import export_json

def main():

    profiles = []

    targets = list_tls_targets()

    total = len(targets)

    for index, target in enumerate(targets, start=1):

        print(
            f"[{index}/{total}] Scanning {target}",
            flush=True,
        )

        target_name, xml, rc, stderr = run_sslscan_xml(target)

        if xml is None:
            continue

        parsed = parse_sslscan_xml(xml)

        profile = BinaryProfile(
            path=target,
            filename=target,
            extension="network",
        )

        profile.detections = [
            {
                "type": "tls",

                "ciphers": extract_ciphers(parsed),

                "client_cas": extract_client_cas(parsed, xml),

                "certificates": extract_certificates_from_parsed(
                    parsed,
                    xml,
                ),
            }
        ]

        profiles.append(profile)

    export_csv(
        profiles,
        output_file="network_protocol.csv",
    )

    json_result = export_json(
        profiles,
        output_file="network_protocol.json",
    )

    return json_result

def run_scan():
    return main()


if __name__ == "__main__":
    main()