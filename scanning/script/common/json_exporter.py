import json
import socket
import platform
from datetime import datetime, timezone


def export_json(profiles, output_file="binaries_used.json"):
    """
    Export BinaryProfile objects to JSON.
    """

    scan = {
        "scanner": "AGCT Scanner",
        "version": "1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "platform": platform.system(),
    }

    binaries = []

    for profile in profiles:

        binaries.append({
            "path": profile.path,
            "filename": profile.filename,
            "extension": profile.extension,
            "language": profile.language,
            "overall_confidence": profile.overall_confidence,
            "crypto_dependencies": profile.crypto_dependencies,
            "detections": [
                {
                    **hit,
                    "detection_source": sorted(list(hit.get("detection_source", [])))
                }
                for hit in profile.detections
            ],
        })

    with open(output_file, "w", encoding="utf-8") as f:
        output = {
            "scan": scan,
            "binaries": binaries,
        }

        json.dump(output, f, indent=4)
    return output