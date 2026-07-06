from sqlalchemy.orm import Session
from app.models.profil import Profil
from app.models.x_profil_tugasan import XProfilTugasan
from app.i18n import t

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
            "message": t("report.profileNotFound")
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
                print(json.dumps(hasil, indent=4))

            # ensure list
            if not isinstance(hasil, list):
                continue

            for item in hasil:

                if not item:
                    continue

                report_rows.append({

                    t("report.columns.profileName"): profile.nama,
                    t("report.columns.taskName"): task.tugasan.nama,
                    t("report.columns.taskCode"): task.tugasan.kod,

                    t("report.columns.agentIp"): host_ip,

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
                })

    # ==========================================
    # NO DATA
    # ==========================================

    if len(report_rows) == 0:
        return {
            "message": t("report.noResults")
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
        "message": t("report.generated"),
        "file": filepath
    }
