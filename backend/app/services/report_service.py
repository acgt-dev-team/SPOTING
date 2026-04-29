from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.profil import Profil
from app.models.x_profil_tugasan import XProfilTugasan
import pandas as pd
import os


def generate_report(db: Session, profil_id: int):
    profile = db.query(Profil).filter(
        Profil.id == profil_id
    ).first()

    if not profile:
        return {"message": "Profile not found"}

    tasks = db.query(XProfilTugasan).filter(
        XProfilTugasan.profil_id == profil_id
    ).all()

    report_data = []

    for task in tasks:
        latest_scan = db.execute(
            text("""
                SELECT data_imbasan, created_at
                FROM hasil_imbasan
                WHERE x_profil_tugasan_id = :id
                ORDER BY created_at DESC
                LIMIT 1
            """),
            {"id": task.id}
        ).fetchone()

        report_data.append({
            "Task Name": task.tugasan.nama,
            "Task Code": task.tugasan.kod,
            "Protocol": task.tugasan.protocol,
            "Status": task.status_id,
            "Latest Scan": latest_scan.created_at if latest_scan else None,
            "Scan Result": str(latest_scan.data_imbasan) if latest_scan else "No Result"
        })

    # DEFAULT → EXCEL
    if profile.report_format == "EXCEL":
        filename = f"report_profile_{profil_id}.xlsx"

        df = pd.DataFrame(report_data)
        df.to_excel(filename, index=False)

        return {
            "message": "Excel report generated",
            "file": filename
        }

    elif profile.report_format == "PDF":
        return {
            "message": "PDF generation coming next"
        }

    return {
        "message": "Invalid format"
    }