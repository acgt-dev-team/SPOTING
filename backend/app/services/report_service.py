from sqlalchemy.orm import Session
from app.models.profil import Profil
from app.models.x_profil_tugasan import XProfilTugasan

import pandas as pd
import os
import json

from sqlalchemy import text


def generate_report(db: Session, profil_id: int):

    profile = db.query(Profil).filter(
        Profil.id == profil_id
    ).first()

    if not profile:
        return {
            "message": "Profile not found"
        }

    tasks = db.query(XProfilTugasan).filter(
        XProfilTugasan.profil_id == profil_id
    ).all()

    report_rows = []

    for task in tasks:

        # ==========================================
        # GET SCAN RESULT FROM EJEN
        # ==========================================
        results = db.execute(
            text("""
                SELECT
                    e.ip_address,
                    h.hasil
                FROM hasil_imbasan h
                JOIN ejen e
                    ON e.id = h.ejen_id
                WHERE h.profil_tugasan_id = :profil_tugasan_id
                AND h.hasil IS NOT NULL
            """),
            {
            "profil_tugasan_id": task.id
            }
        ).fetchall()

        for row in results:

            host_ip = row.ip_address

            hasil = row.hasil

            if not hasil:
                continue

            if isinstance(hasil, str):
                hasil = json.loads(hasil)

            # ensure list
            if not isinstance(hasil, list):
                continue

            for item in hasil:

                if not item:
                    continue

                cbom = item.get("cbom_data", {})

                if not cbom:
                    continue

                report_rows.append({

                    "Profile Name": profile.nama,
                    "Task Name": task.tugasan.nama,
                    "Task Code": task.tugasan.kod,

                    "Agent IP": host_ip,

                    "Path": cbom.get("path"),
                    "File Type": cbom.get("file_type"),

                    "Algorithm": cbom.get("algorithm"),
                    "Key Size": cbom.get("key_size"),
                    "Curve": cbom.get("curve"),

                    "RSA Modulus Fingerprint":
                        cbom.get("rsa_modulus_fingerprint"),

                    "RSA Exponent":
                        cbom.get("rsa_exponent"),

                    "Signature Algorithm":
                        cbom.get("signature_algorithm"),

                    "Subject":
                        cbom.get("subject"),

                    "Issuer":
                        cbom.get("issuer"),

                    "Serial":
                        cbom.get("serial"),

                    "Not Before":
                        cbom.get("not_before"),

                    "Not After":
                        cbom.get("not_after"),

                    "SHA1":
                        cbom.get("fingerprint_sha1"),

                    "SHA256":
                        cbom.get("fingerprint_sha256"),
                })

    # ==========================================
    # NO DATA
    # ==========================================

    if len(report_rows) == 0:
        return {
            "message": "No scan results found"
        }

    # ==========================================
    # EXPORT EXCEL
    # ==========================================

    df = pd.DataFrame(report_rows)

    os.makedirs("reports", exist_ok=True)

    safe_name = profile.nama.replace(" ", "_")

    filepath = f"reports/{safe_name}.xlsx"

    df.to_excel(filepath, index=False)

    return {
        "message": "Report generated",
        "file": filepath
    }