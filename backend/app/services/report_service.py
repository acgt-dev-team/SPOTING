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
    """
    Entry point for report generation.
    """

    profile = (
        db.query(Profil)
        .filter(Profil.id == profil_id)
        .first()
    )

    if not profile:
        return {
            "message": t("report.profileNotFound")
        }

    scan_entries = _collect_scan_entries(db, profil_id)

    if not scan_entries:
        return {
            "message": t("report.noResults")
        }

    if report_format == CYCLONEDX_REPORT_FORMAT:
        return _generate_cyclonedx_report(
            profile,
            scan_entries,
        )

    return _generate_excel_report(
        profile,
        scan_entries,
    )


def _collect_scan_entries(
    db: Session,
    profil_id: int,
):
    """
    Collect every scan result belonging to a profile.
    """

    tasks = (
        db.query(XProfilTugasan)
        .filter(
            XProfilTugasan.profil_id == profil_id
        )
        .all()
    )

    scan_entries = []

    for task in tasks:

        rows = db.execute(
            text(
                """
                SELECT
                    e.ip_address,
                    h.hasil
                FROM hasil_imbasan h
                JOIN ejen e
                    ON e.id = h.ejen_id
                WHERE h.profil_tugasan_id = :profil_tugasan_id
                """
            ),
            {
                "profil_tugasan_id": task.id
            },
        ).fetchall()

        for row in rows:

            hasil = _parse_scan_result(row.hasil)

            if not hasil:
                continue

            scan_entries.extend(
                _normalize_scan_result(
                    hasil=hasil,
                    agent_ip=row.ip_address,
                    task=task.tugasan,
                )
            )

    return scan_entries


def _normalize_scan_result(
    hasil: dict,
    agent_ip: str,
    task,
):
    """
    Convert every scanner output into one common structure.

    Every top-level array except 'scan' becomes a report category.
    """

    entries = []

    if not isinstance(hasil, dict):
        return entries

    metadata = hasil.get("scan", {})

    for category, value in hasil.items():

        #
        # Skip metadata
        #
        if category == "scan":
            continue

        #
        # We only care about arrays
        #
        if not isinstance(value, list):
            continue

        for item in value:

            if not isinstance(item, dict):
                continue

            #
            # Choose the best display name
            #
            resource = (
                item.get("filename")
                or item.get("name")
                or item.get("path")
                or item.get("process")
                or item.get("subject")
                or item.get("hostname")
                or category
            )

            entries.append(
                {
                    "category": category,
                    "agent_ip": agent_ip,
                    "task": task,
                    "resource": resource,
                    "metadata": metadata,
                    "properties": item,
                }
            )

    return entries


def _parse_scan_result(hasil):
    """
    Parse JSON stored in PostgreSQL.
    """

    #
    # PostgreSQL JSON column
    #
    if isinstance(hasil, dict):
        return hasil

    #
    # TEXT column
    #
    if isinstance(hasil, str):
        try:
            return json.loads(hasil)
        except json.JSONDecodeError:
            return None

    return None 

def _generate_excel_report(
    profile: Profil,
    scan_entries: list[dict],
):
    """
    Generate a generic Excel report.

    Every property from every scan category becomes a column automatically.
    """

    rows = []

    for entry in scan_entries:

        metadata = entry.get("metadata", {})
        properties = entry.get("properties", {})

        row = {
            "Profile Name": profile.nama,
            "Profile Code": profile.kod,
            "Task Name": entry["task"].nama,
            "Task Code": entry["task"].kod,
            "Agent IP": entry["agent_ip"],
            "Category": entry["category"],
            "Resource": entry["resource"],

            # Scanner metadata
            "Scanner": metadata.get("scanner"),
            "Scanner Version": metadata.get("version"),
            "Hostname": metadata.get("hostname"),
            "Platform": metadata.get("platform"),
            "Scan Timestamp": metadata.get("timestamp"),
        }

        #
        # Add every property dynamically
        #
        for key, value in properties.items():

            if value is None:
                row[key] = ""
                continue

            #
            # Lists become JSON strings
            #
            if isinstance(value, list):
                row[key] = json.dumps(
                    value,
                    ensure_ascii=False,
                )
                continue

            #
            # Nested dictionaries become JSON strings
            #
            if isinstance(value, dict):
                row[key] = json.dumps(
                    value,
                    ensure_ascii=False,
                )
                continue

            row[key] = value

        rows.append(row)

    #
    # Build dataframe
    #
    dataframe = pd.DataFrame(rows)

    #
    # Sort columns nicely
    #
    preferred_columns = [
        "Profile Name",
        "Profile Code",
        "Task Name",
        "Task Code",
        "Agent IP",
        "Category",
        "Resource",
        "Scanner",
        "Scanner Version",
        "Hostname",
        "Platform",
        "Scan Timestamp",
    ]

    dynamic_columns = [
        column
        for column in dataframe.columns
        if column not in preferred_columns
    ]

    dataframe = dataframe[
        preferred_columns + sorted(dynamic_columns)
    ]

    #
    # Save report
    #
    os.makedirs("reports", exist_ok=True)

    filename = (
        f"{_safe_profile_name(profile.nama)}"
        "_report.xlsx"
    )

    filepath = os.path.join(
        "reports",
        filename,
    )

    with pd.ExcelWriter(
        filepath,
        engine="openpyxl",
    ) as writer:

        dataframe.to_excel(
            writer,
            sheet_name="Results",
            index=False,
        )

        worksheet = writer.sheets["Results"]

        #
        # Auto-adjust column widths
        #
        for column_cells in worksheet.columns:

            max_length = 0

            column = column_cells[0].column_letter

            for cell in column_cells:

                try:
                    value = str(cell.value)

                    if len(value) > max_length:
                        max_length = len(value)

                except Exception:
                    pass

            worksheet.column_dimensions[column].width = min(
                max_length + 3,
                60,
            )

    return {
        "message": t("report.generated"),
        "file": filepath,
        "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

def _generate_cyclonedx_report(
    profile: Profil,
    scan_entries: list[dict],
):
    """
    Generate a generic CycloneDX SBOM from normalized scan entries.
    """

    components = []

    for index, entry in enumerate(scan_entries, start=1):

        metadata = entry.get("metadata", {})
        properties = entry.get("properties", {})

        resource = entry["resource"] or f"resource-{index}"

        component_hash = sha256(
            f"{entry['category']}|{resource}".encode("utf-8")
        ).hexdigest()[:16]

        component = {
            "bom-ref": f"spoting-{component_hash}",
            "type": "application",
            "name": resource,
            "properties": [],
        }

        #
        # Standard SPOTING properties
        #
        _add_property(
            component,
            "spoting:category",
            entry["category"],
        )

        _add_property(
            component,
            "spoting:agent-ip",
            entry["agent_ip"],
        )

        _add_property(
            component,
            "spoting:task-name",
            entry["task"].nama,
        )

        _add_property(
            component,
            "spoting:task-code",
            entry["task"].kod,
        )

        #
        # Scanner metadata
        #
        for key, value in metadata.items():

            _add_property(
                component,
                f"spoting:scan:{key}",
                value,
            )

        #
        # Scan properties
        #
        for key, value in properties.items():

            if isinstance(value, (dict, list)):
                value = json.dumps(
                    value,
                    ensure_ascii=False,
                )

            _add_property(
                component,
                f"spoting:{key}",
                value,
            )

        components.append(component)

    #
    # Metadata component
    #
    metadata_component = {
        "type": "application",
        "name": profile.nama,
        "properties": [],
    }

    _add_property(
        metadata_component,
        "spoting:profile-code",
        profile.kod,
    )

    bom = {
        "$schema": "https://cyclonedx.org/schema/bom-1.5.schema.json",
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:{uuid4()}",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat().replace("+00:00", "Z"),
            "component": metadata_component,
        },
        "components": components,
    }

    os.makedirs(
        "reports",
        exist_ok=True,
    )

    filename = (
        f"{_safe_profile_name(profile.nama)}"
        "_cyclonedx.json"
    )

    filepath = os.path.join(
        "reports",
        filename,
    )

    with open(
        filepath,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            bom,
            file,
            indent=2,
            ensure_ascii=False,
        )

    return {
        "message": t("report.generated"),
        "file": filepath,
        "media_type": "application/vnd.cyclonedx+json",
    } 

def _add_property(
    component: dict,
    name: str,
    value,
):
    """
    Add a CycloneDX property if it contains a value.
    """

    if value is None:
        return

    if value == "":
        return

    #
    # Convert complex objects into JSON strings
    #
    if isinstance(value, (dict, list)):
        value = json.dumps(
            value,
            ensure_ascii=False,
        )

    property_value = str(value)

    new_property = {
        "name": name,
        "value": property_value,
    }

    #
    # Avoid duplicate properties
    #
    if new_property not in component["properties"]:
        component["properties"].append(
            new_property
        )


def _safe_profile_name(name: str):
    """
    Convert profile name into a filesystem-safe filename.
    """

    if not name:
        return "profil"

    safe_name = "".join(
        character
        if character.isalnum() or character in {"-", "_"}
        else "_"
        for character in name
    )

    while "__" in safe_name:
        safe_name = safe_name.replace("__", "_")

    safe_name = safe_name.strip("_")

    return safe_name or "profil"
