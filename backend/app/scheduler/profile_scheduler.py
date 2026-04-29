from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.profil import Profil
from app.models.x_profil_tugasan import XProfilTugasan
from app.services.tugasan_service import execute_scan


# ==========================================
# Scheduler instance
# ==========================================
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

        tasks = db.query(XProfilTugasan).filter(
            XProfilTugasan.profil_id == profile.id
        ).all()

        print(f"Tasks found: {len(tasks)}")

        if not tasks:
            print("No tasks assigned to this profile")
            return

        for task in tasks:
            print(f"Executing task ID: {task.id}")

            try:
                result = execute_scan(
                    db=db,  # FIXED HERE
                    profil_tugasan_id=task.id,
                    penjadualan=True
                )

                print(f"Scan result: {result}")

            except Exception as e:
                print(
                    f"Failed executing task {task.id}: {str(e)}"
                )

    except Exception as e:
        print(f"Scheduler error: {str(e)}")

    finally:
        db.close()


# ==========================================
# Load all scheduled profiles from DB
# ==========================================
def load_profile_jobs():
    db: Session = SessionLocal()

    try:
        profiles = db.query(Profil).filter(
            Profil.is_scheduled == True
        ).all()

        print(f"Found {len(profiles)} scheduled profiles")

        for profile in profiles:

            if not profile.cron_expression:
                print(
                    f"Profile {profile.id} has no cron expression"
                )
                continue

            parts = profile.cron_expression.split()

            if len(parts) != 5:
                print(
                    f"Invalid cron expression for profile {profile.id}: {profile.cron_expression}"
                )
                continue

            minute, hour, day, month, day_of_week = parts

            scheduler.add_job(
                run_single_profile,
                trigger=CronTrigger(
                    minute=minute,
                    hour=hour,
                    day=day,
                    month=month,
                    day_of_week=day_of_week
                ),
                args=[profile.id],
                id=f"profile_{profile.id}",
                replace_existing=True
            )

            print(
                f"Scheduled profile {profile.nama} "
                f"with cron: {profile.cron_expression}"
            )

    except Exception as e:
        print(f"Failed loading scheduler jobs: {str(e)}")

    finally:
        db.close()