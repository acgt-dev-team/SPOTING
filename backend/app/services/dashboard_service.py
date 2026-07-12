from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.organisasi import Organisasi
from app.models.sub_organisasi import SubOrganisasi
from app.models.tapak import Tapak
from app.models.profil import Profil
from app.models.tugasan import Tugasan
from app.models.x_profil_tugasan import XProfilTugasan



def get_dashboard_stats(db: Session):

    organisasi_count = db.query(func.count(Organisasi.id)).scalar()
    sub_organisasi_count = db.query(func.count(SubOrganisasi.id)).scalar()
    tapak_count = db.query(func.count(Tapak.id)).scalar()
    profil_count = db.query(func.count(Profil.id)).scalar()
    tugasan_count = db.query(func.count(Tugasan.id)).scalar()

    return {
        "organisasi": organisasi_count or 0,
        "sub_organisasi": sub_organisasi_count or 0,
        "tapak": tapak_count or 0,
        "profil": profil_count or 0,
        "tugasan": tugasan_count or 0
    }

def get_organization_performance(db: Session):
    results = (
        db.query(
            Organisasi,
            func.count(XProfilTugasan.id).label("total"),
            func.count(XProfilTugasan.id).filter(
                XProfilTugasan.status_id == 3
            ).label("done")
        )
        .outerjoin(SubOrganisasi, SubOrganisasi.organisasi_id == Organisasi.id)
        .outerjoin(Tapak, Tapak.sub_organisasi_id == SubOrganisasi.id)
        .outerjoin(Profil, Profil.tapak_id == Tapak.id)
        .outerjoin(XProfilTugasan, XProfilTugasan.profil_id == Profil.id)
        .group_by(Organisasi.id)
        .all()
    )

    response = []

    for i, (org, total, done) in enumerate(results, start=1):
        response.append({
            "bil": i,
            "nama": org.nama,
            "total": total or 0,
            "done": done or 0
        })

    return response


def _normalize_profile_status(status):
    value = (status or "").strip().lower()

    if value in ("belum", "belum dimulakan"):
        return "not_started"

    if value == "in process":
        return "in_process"

    if value == "execution completed":
        return "completed"

    if value == "gagal":
        return "failed"

    if value == "telah dijadualkan":
        return "scheduled"

    return "unknown"


def _profile_rows(db: Session):
    task_counts = (
        db.query(
            XProfilTugasan.profil_id.label("profil_id"),
            func.count(XProfilTugasan.id).label("task_count")
        )
        .group_by(XProfilTugasan.profil_id)
        .subquery()
    )

    return (
        db.query(
            Profil,
            Tapak,
            SubOrganisasi,
            Organisasi,
            func.coalesce(task_counts.c.task_count, 0).label("task_count")
        )
        .join(Tapak, Profil.tapak_id == Tapak.id)
        .join(SubOrganisasi, Tapak.sub_organisasi_id == SubOrganisasi.id)
        .join(Organisasi, SubOrganisasi.organisasi_id == Organisasi.id)
        .outerjoin(task_counts, task_counts.c.profil_id == Profil.id)
        .all()
    )


def _serialize_profile(row):
    profil, tapak, sub_organisasi, organisasi, task_count = row

    return {
        "id": profil.id,
        "kod": profil.kod,
        "nama": profil.nama,
        "tapak_id": tapak.id,
        "tapak": tapak.nama,
        "sub_organisasi_id": sub_organisasi.id,
        "sub_organisasi": sub_organisasi.nama,
        "organisasi_id": organisasi.id,
        "organisasi": organisasi.nama,
        "task_count": int(task_count or 0),
        "execution_status": profil.execution_status,
        "execution_type": profil.execution_type,
        "scheduled_at": profil.scheduled_at,
        "cron_enabled": bool(profil.cron_enabled),
        "frequency": profil.frequency,
        "cron_expression": profil.cron_expression,
        "updated_at": profil.kemaskini_pada or profil.cipta_pada
    }


def get_profile_health(db: Session):
    rows = _profile_rows(db)

    counts = {
        "not_started": 0,
        "in_process": 0,
        "scheduled": 0,
        "completed": 0,
        "failed": 0,
        "unknown": 0
    }

    profiles = []

    for row in rows:
        profile = _serialize_profile(row)
        status_key = _normalize_profile_status(profile["execution_status"])

        counts[status_key] = counts.get(status_key, 0) + 1
        profile["status_key"] = status_key
        profiles.append(profile)

    failed_profiles = [
        profile for profile in profiles
        if profile["status_key"] == "failed"
    ]

    failed_profiles.sort(
        key=lambda profile: profile["updated_at"] or datetime.min,
        reverse=True
    )

    scheduled_profiles = [
        profile for profile in profiles
        if (
            profile["status_key"] == "scheduled"
            or profile["cron_enabled"]
            or (
                profile["execution_type"] == "SCHEDULED"
                and profile["scheduled_at"] is not None
            )
        )
    ]

    scheduled_profiles.sort(
        key=lambda profile: profile["scheduled_at"] or datetime.max
    )

    recent_profiles = sorted(
        profiles,
        key=lambda profile: profile["updated_at"] or datetime.min,
        reverse=True
    )

    return {
        "counts": counts,
        "profiles": profiles,
        "failed_profiles": failed_profiles[:5],
        "scheduled_profiles": scheduled_profiles[:5],
        "recent_profiles": recent_profiles[:5]
    }
