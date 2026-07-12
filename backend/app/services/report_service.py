from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from uuid import uuid4

import json
import os

import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.i18n import t
from app.models.profil import Profil
from app.models.x_profil_tugasan import XProfilTugasan


DEFAULT_REPORT_FORMAT = "default"
CYCLONEDX_REPORT_FORMAT = "cyclonedx"


def generate_report(
    db: Session,
    profil_id: int,
    report_format: str = DEFAULT_REPORT_FORMAT,
):
    profile = db.query(Profil).filter(Profil.id == profil_id).first()

    if not profile:
        return {"message": t("report.profileNotFound")}

    scan_entries = _collect_scan_entries(db, profil_id)

    if not scan_entries:
        return {"message": t("report.noResults")}

    if report_format == CYCLONEDX_REPORT_FORMAT:
        return _generate_cyclonedx_report(profile, scan_entries)

    return _generate_excel_report(profile, scan_entries)


def _collect_scan_entries(db: Session, profil_id: int):
    tasks = (
        db.query(XProfilTugasan)
        .filter(XProfilTugasan.profil_id == profil_id)
        .all()
    )
    scan_entries = []

    for task in tasks:
        results = db.execute(
            text(
                """
                SELECT
                    e.ip_address,
                    h.hasil
                FROM hasil_imbasan h
                JOIN ejen e ON e.id = h.ejen_id
                WHERE h.profil_tugasan_id = :profil_tugasan_id
                    AND h.hasil IS NOT NULL
                """
            ),
            {"profil_tugasan_id": task.id},
        ).fetchall()

        for row in results:
            hasil = _parse_scan_result(row.hasil)

            if not isinstance(hasil, list):
                continue

            for item in hasil:
                if isinstance(item, dict) and item:
                    scan_entries.append(
                        {
                            "agent_ip": row.ip_address,
                            "result": item,
                            "task": task.tugasan,
                        }
                    )

    return scan_entries


def _parse_scan_result(hasil):
    if not isinstance(hasil, str):
        return hasil

    try:
        return json.loads(hasil)
    except json.JSONDecodeError:
        return None


def _generate_excel_report(profile: Profil, scan_entries: list[dict]):
    report_rows = []

    for entry in scan_entries:
        task = entry["task"]
        item = entry["result"]

        report_rows.append(
            {
                t("report.columns.profileName"): profile.nama,
                t("report.columns.taskName"): task.nama,
                t("report.columns.taskCode"): task.kod,
                t("report.columns.agentIp"): entry["agent_ip"],
                t("report.columns.process"): item.get("Process"),
                t("report.columns.pid"): item.get("PID"),
                t("report.columns.protocol"): item.get("Protocol"),
                t("report.columns.remoteIp"): item.get("RemoteIP"),
                t("report.columns.remotePort"): item.get("RemotePort"),
                t("report.columns.executablePath"): item.get("ExecutablePath"),
                t("report.columns.role"): item.get("Role"),
                t("report.columns.cryptoDetails"): item.get("CryptoDetails"),
                t("report.columns.scriptPath"): item.get("ScriptPath"),
                t("report.columns.scanTime"): item.get("ScanTimeUTC"),
            }
        )

    os.makedirs("reports", exist_ok=True)
    filepath = f"reports/{_safe_profile_name(profile.nama)}.xlsx"
    pd.DataFrame(report_rows).to_excel(filepath, index=False)

    return {
        "message": t("report.generated"),
        "file": filepath,
        "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }


def _generate_cyclonedx_report(profile: Profil, scan_entries: list[dict]):
    components = {}

    for index, entry in enumerate(scan_entries, start=1):
        item = entry["result"]
        task = entry["task"]
        executable_path = item.get("ExecutablePath")
        process_name = item.get("Process")
        component_name = (
            str(process_name).strip()
            if process_name
            else Path(str(executable_path)).name
            if executable_path
            else task.nama or f"scan-result-{index}"
        )
        component_key = f"{component_name}|{executable_path or ''}"

        if component_key not in components:
            component_hash = sha256(component_key.encode("utf-8")).hexdigest()[:16]
            components[component_key] = {
                "bom-ref": f"spoting-component-{component_hash}",
                "type": "application",
                "name": component_name,
                "properties": [],
            }

        component = components[component_key]
        _add_property(component, "spoting:executable-path", executable_path)
        _add_property(component, "spoting:process-id", item.get("PID"))
        _add_property(component, "spoting:agent-ip", entry["agent_ip"])
        _add_property(component, "spoting:task-name", task.nama)
        _add_property(component, "spoting:task-code", task.kod)
        _add_property(component, "spoting:connection", _connection_value(item))
        _add_property(component, "spoting:role", item.get("Role"))
        _add_property(component, "spoting:crypto-details", item.get("CryptoDetails"))
        _add_property(component, "spoting:script-path", item.get("ScriptPath"))
        _add_property(component, "spoting:scan-time", item.get("ScanTimeUTC"))

    metadata_component = {
        "type": "application",
        "name": profile.nama,
        "properties": [],
    }
    _add_property(metadata_component, "spoting:profile-code", profile.kod)

    bom = {
        "$schema": "https://cyclonedx.org/schema/bom-1.5.schema.json",
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:{uuid4()}",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "component": metadata_component,
        },
        "components": list(components.values()),
    }

    os.makedirs("reports", exist_ok=True)
    filepath = f"reports/{_safe_profile_name(profile.nama)}-cyclonedx.json"

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(bom, file, ensure_ascii=False, indent=2)

    return {
        "message": t("report.generated"),
        "file": filepath,
        "media_type": "application/vnd.cyclonedx+json",
    }


def _add_property(component: dict, name: str, value):
    if value is None or value == "":
        return

    property_value = str(value)
    new_property = {"name": name, "value": property_value}

    if new_property not in component["properties"]:
        component["properties"].append(new_property)


def _connection_value(item: dict):
    remote_ip = item.get("RemoteIP")
    remote_port = item.get("RemotePort")
    protocol = item.get("Protocol")

    if not any((remote_ip, remote_port, protocol)):
        return None

    endpoint = str(remote_ip or "unknown")
    if remote_port not in (None, ""):
        endpoint = f"{endpoint}:{remote_port}"

    return f"{protocol}://{endpoint}" if protocol else endpoint


def _safe_profile_name(name: str):
    safe_name = "".join(
        character if character.isalnum() or character in {"-", "_"} else "_"
        for character in (name or "profil")
    )

    return safe_name.strip("_") or "profil"
