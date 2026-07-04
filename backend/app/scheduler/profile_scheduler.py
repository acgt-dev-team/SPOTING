from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.session import SessionLocal
from app.models.profil import Profil
from app.models.x_profil_tugasan import XProfilTugasan
from app.services.tugasan_service import execute_scan


scheduler = BackgroundScheduler()


# ==========================================
# Run single profile
# ==========================================
def run_single_profile(profile_id: int):
    db: Session = SessionLocal()

    try:
        profile = db.query(Profil).filter(
            Profil.id == profile_id
        ).first()

        if not profile:
            print(f"Profile {profile_id} not found")
            return

        print(f"\nRunning profile: {profile.nama}")

        # ✅ set status to in process
        profile.execution_status = "in process"
        db.commit()

        tasks = db.query(
            XProfilTugasan
        ).filter(
            XProfilTugasan.profil_id == profile.id
        ).all()

        if not tasks:
            print("No tasks found")
            return

        profile.execution_status = "in process"
        db.commit()

        print("Released profile to agent.")

    except Exception as e:
        print(f"Scheduler error: {str(e)}")

        if profile:
            profile.execution_status = "gagal"
            db.commit()

    finally:
        db.close()


# ==========================================
# Load scheduled jobs
# ==========================================
def load_profile_jobs():
    db: Session = SessionLocal()

    try:
        profiles = db.query(Profil).filter(
            Profil.execution_type == "SCHEDULED",
            Profil.scheduled_at != None,
            Profil.execution_status == "telah dijadualkan"
        ).all()

        print(f"Found {len(profiles)} scheduled profiles")

        for profile in profiles:
            scheduler.add_job(
                run_single_profile,
                'date',
                run_date=profile.scheduled_at,
                args=[profile.id],
                id=f"profile_{profile.id}",
                replace_existing=True
            )

            print(f"Scheduled profile {profile.nama} at {profile.scheduled_at}")

    except Exception as e:
        print(f"Scheduler load error: {str(e)}")

    finally:
        db.close()