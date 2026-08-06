from sqlalchemy.orm import Session
from app.models.tugasan import Tugasan
from app.models.x_profil_tugasan import XProfilTugasan
from app.models.profil import Profil
from app.i18n import t

import requests
import json

from sqlalchemy import text
from fastapi import HTTPException
from app.services.profile_task_agent_service import (
    create_task_agent_assignments
)
from app.models.x_profil_ejen import XProfilEjen
from app.models.x_profil_tugasan_ejen import XProfilTugasanEjen
from app.services.profile_agent_service import (
    assign_agents_to_profile
)



# ==========================================
# GET ASSIGNED TASKS BY PROFILE
# ==========================================
def get_tugasan_by_profil(db: Session, profil_id: int):
    results = (
        db.query(XProfilTugasan)
        .filter(XProfilTugasan.profil_id == profil_id)
        .all()
    )

    response = []

    for item in results:
    
        agent_count = (
            db.query(XProfilTugasanEjen)
            .filter(
                XProfilTugasanEjen.profil_tugasan_id == item.id
            )
            .count()
        )

        completed_agent_count = (
            db.query(XProfilTugasanEjen)
            .filter(
                XProfilTugasanEjen.profil_tugasan_id == item.id,
                XProfilTugasanEjen.status == "Completed"
            )
            .count()
        )
        
        response.append({
            "profil_tugasan_id": item.id,
            "id": item.tugasan.id,
            "nama": item.tugasan.nama,
            "kod": item.tugasan.kod,
            "keterangan": item.tugasan.keterangan,
            "protocol": item.tugasan.protocol,
            "ip_start": item.tugasan.ip_start,
            "ip_end": item.tugasan.ip_end,
            "status": item.status_id,

            "agent_count": agent_count,
            "completed_agent_count": completed_agent_count
        })

    return response

# ==========================================
# ASSIGN TASK TO PROFILE
# ==========================================
def assign_tugasan_to_profil(
    db: Session,
    profil_id: int,
    tugasan_id: int
):
    existing = (
        db.query(XProfilTugasan)
        .filter_by(
            profil_id=profil_id,
            tugasan_id=tugasan_id
        )
        .first()
    )

    if existing:
        return {
            "message": t("task.alreadyAssigned")
        }

    # ------------------------------------------
    # Create profile task
    # ------------------------------------------
    new_item = XProfilTugasan(
        profil_id=profil_id,
        tugasan_id=tugasan_id,
        status_id=1
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)


    print("\n========== ASSIGN TASK ==========")
    print(f"Profile ID : {profil_id}")
    print(f"Task ID    : {tugasan_id}")

    # ------------------------------------------
    # Load profile
    # ------------------------------------------
    profile = (
        db.query(Profil)
        .filter(
            Profil.id == profil_id
        )
        .first()
    )

    if not profile:
        print("Profile not found!")
        return {
            "message": t("task.profileNotFound")
        }

    print("Execution Type :", profile.execution_type)
    print("Status BEFORE  :", profile.execution_status)

    # ------------------------------------------
    # New task means all assigned agents
    # should check this profile again
    # ------------------------------------------
    profile.execution_status = "in process"

    profile_agents = (
        db.query(XProfilEjen)
        .filter(
            XProfilEjen.profil_id == profile.id
        )
        .all()
    )

    for agent in profile_agents:

        # Only reopen completed agents
        if agent.status == "Completed":

            agent.status = "Pending"
            agent.started_at = None
            agent.completed_at = None

    db.commit()
    db.refresh(profile)
    
    # ------------------------------------------
    # Immediate profile
    # ------------------------------------------
    if profile.execution_type == "IMMEDIATE":

        profile.execution_status = "in process"

        db.commit()
        db.refresh(profile)

        # Always ensure profile-agent assignments exist.
        # Safe because assign_agents_to_profile() is idempotent.
        assign_agents_to_profile(
            db=db,
            profile_id=profile.id
        )


    # ------------------------------------------
    # Scheduled profile
    # ------------------------------------------
    elif profile.execution_type == "SCHEDULED":

        profile.execution_status = "telah dijadualkan"

    db.commit()
    db.refresh(profile)
    
    # ------------------------------------------
    # Ensure Task-Agent rows exist
    # ------------------------------------------
    create_task_agent_assignments(
        db=db,
        profil_id=profil_id
    )

    print("Status AFTER   :", profile.execution_status)
    print("=================================\n")

    return {
        "message": t("task.assigned"),
        "profil_tugasan_id": new_item.id
    }


# ==========================================
# CREATE TASK
# ==========================================
def create_tugasan(db: Session, data: dict):

    existing = db.query(Tugasan).filter(
        Tugasan.nama == data["nama"]
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=t("task.exists")
        )
    
    new_tugasan = Tugasan(
        nama=data["nama"],
        kod=data["kod"],
        keterangan=data.get("keterangan"),
        jenis_id=data["jenis_id"],
        protocol=data.get("protocol"),
        ip_start=data.get("ip_start"),
        ip_end=data.get("ip_end"),
        aktif=data.get("aktif", True)
    )

    db.add(new_tugasan)
    db.commit()
    db.refresh(new_tugasan)

    return {
        "id": new_tugasan.id,
        "nama": new_tugasan.nama,
        "kod": new_tugasan.kod,
        "keterangan": new_tugasan.keterangan,
        "jenis_id": new_tugasan.jenis_id,
        "protocol": new_tugasan.protocol,
        "ip_start": new_tugasan.ip_start,
        "ip_end": new_tugasan.ip_end,
        "aktif": new_tugasan.aktif
    }


# ==========================================
# UPDATE TASK
# ==========================================
def update_tugasan(
    db: Session,
    tugasan_id: int,
    data: dict
):
    tugasan = db.query(Tugasan).filter(
        Tugasan.id == tugasan_id
    ).first()

    if not tugasan:
        raise HTTPException(
            status_code=404,
            detail=t("task.notFound")
        )

    tugasan.nama = data["nama"]
    tugasan.kod = data["kod"]
    tugasan.keterangan = data.get("keterangan")
    tugasan.jenis_id = data["jenis_id"]
    tugasan.protocol = data.get("protocol")
    tugasan.ip_start = data.get("ip_start")
    tugasan.ip_end = data.get("ip_end")
    tugasan.aktif = data.get("aktif", True)

    db.commit()
    db.refresh(tugasan)

    return {
        "message": t("task.updated"),
        "id": tugasan.id
    }


# ==========================================
# REMOVE TASK FROM PROFILE
# ==========================================
def remove_tugasan_from_profil(
    db: Session,
    profil_id: int,
    tugasan_id: int
):
    item = db.query(XProfilTugasan).filter_by(
        profil_id=profil_id,
        tugasan_id=tugasan_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail=t("task.assignmentNotFound")
        )

    # prevent deletion if scan history exists
    existing_scan = db.execute(
    text("""
        SELECT id
        FROM ejen
        WHERE tugasan_id = :id
        AND hasil_imbasan IS NOT NULL
        LIMIT 1
    """),
    {"id": tugasan_id}
).fetchone()

    if existing_scan:
        raise HTTPException(
            status_code=400,
            detail=t("task.cannotRemoveWithHistory")
        )

    db.delete(item)
    db.commit()

    return {
        "message": t("task.removed")
    }


# ==========================================
# GET ALL TASKS
# ==========================================
def get_all_tugasan(db: Session):
    tugasan = db.query(Tugasan).all()

    return [
        {
            "id": t.id,
            "nama": t.nama,
            "kod": t.kod,
            "keterangan": t.keterangan,
            "protocol": t.protocol,
            "ip_start": t.ip_start,
            "ip_end": t.ip_end,
            "aktif": bool(t.aktif) if t.aktif is not None else False,
            "jenis_id": t.jenis_id
        }
        for t in tugasan
    ]


# ==========================================
# EXECUTE SCAN
# ==========================================
def execute_scan(
    db: Session,
    profil_tugasan_id: int,
    penjadualan: bool = False
):
    url = "http://127.0.0.1:9000/pengguna/imbas"

    task = db.query(XProfilTugasan).filter(
        XProfilTugasan.id == profil_tugasan_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail=t("task.notFound")
        )

    try:
        # -------------------------------
        # set IN PROGRESS
        # -------------------------------
        task.status_id = 2
        db.commit()

        payload = {
            "profil_tugasan_id": profil_tugasan_id,
            "penjadualan": penjadualan
        }

        response = requests.post(
            url,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        print("Response text:", response.text)
        print("Response status:", response.status_code)

        scan_result = response.json()

        protocol = task.tugasan.protocol

        print("Protocol:", protocol)
        print("Raw scan result:", scan_result)

        # parser logic here later

        if scan_result is None:
            scan_result = {
                "message": t("task.scanExecuted"),
                "note": t("task.externalScannerEmpty")
            }

        print("Raw scan result:", scan_result)

        print("Scan completed successfully")

        # -------------------------------
        # set COMPLETED
        # -------------------------------
        task.status_id = 3
        db.commit()

        return {
            "success": True,
            "message": t("task.scanCompleted"),
            "data": scan_result
        }

    except requests.exceptions.RequestException as e:
        task.status_id = 4
        db.commit()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    except Exception as e:
        task.status_id = 4
        db.commit()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
