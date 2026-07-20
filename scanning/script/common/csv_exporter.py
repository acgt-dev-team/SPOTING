import csv


def export_csv(profiles, output_file="binaries_used.csv"):
    """
    Export BinaryProfile objects into the current CSV format.
    """

    with open(output_file, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "resource",
            "resource_type",
            "category",
            "item",
            "property",
            "value",
            "evidence",
            "confidence",
            "severity",
        ])

        for profile in profiles:

            # --------------------------------------------------
            # No detections
            # --------------------------------------------------
            if not profile.detections:

                writer.writerow([
                    profile.path,
                    profile.extension,
                    "binary",
                    "crypto-library",
                    "dependency",
                    ",".join(profile.crypto_dependencies),
                    "import table",
                    "",
                    "info",
                ])

                continue

            # --------------------------------------------------
            # Process detections
            # --------------------------------------------------
            for hit in profile.detections:

                # ==================================================
                # Certificate / Private Key
                # ==================================================
                if hit.get("type") in ("certificate", "private_key"):

                    writer.writerow([
                        profile.path,
                        profile.extension,
                        hit["type"],
                        hit["algorithm"],
                        "key_size",
                        hit["key_size"],
                        hit.get("fingerprint_sha256", ""),
                        "",
                        "info",
                    ])

                    continue

                # ==================================================
                # Network Application
                # ==================================================
                if hit.get("type") == "network_application":

                    writer.writerow([
                        profile.path,
                        profile.extension,
                        "network",
                        hit["protocol"],
                        "connection",
                        f'{hit["remote_ip"]}:{hit["remote_port"]}',
                        hit["process"],
                        "",
                        "info",
                    ])

                    continue

                # ==================================================
                # IPsec Service
                # ==================================================
                if hit.get("type") == "ipsec_service":

                    writer.writerow([
                        profile.path,
                        profile.extension,
                        "network",
                        "IPsec",
                        "service",
                        hit["crypto"],
                        "",
                        "",
                        "info",
                    ])

                    continue

                # ==================================================
                # Crypto detections
                # ==================================================
                if hit.get("primitive") == "multiple":
                    continue

                params = hit.get("parameters", {})
                key_len = params.pop("keyLength", "unknown")

                if key_len != "unknown":
                    property_name = "key_length"
                    value = key_len
                else:
                    property_name = "detected"

                    if hit.get("apis"):
                        value = ",".join(sorted(hit["apis"]))
                    else:
                        value = "yes"

                severity = "warning" if hit.get("deprecated") else "info"

                writer.writerow([
                    profile.path,
                    profile.extension,
                    hit["primitive"],
                    hit["algorithm"],
                    property_name,
                    value,
                    ",".join(sorted(hit["detection_source"])),
                    hit.get("confidence", ""),
                    severity,
                ])