from sqlalchemy.orm import Session

from backend.app.models.pelanggan import Pelanggan
from backend.app.models.organisasi import Organisasi
from backend.app.models.sub_organisasi import SubOrganisasi
from backend.app.models.tapak import Tapak
from backend.app.models.profil import Profil
from backend.app.models.tugasan import Tugasan
from backend.app.utils.logger import logger


def generate_kod(name: str) -> str:
    """Convert name into kod format"""
    return name.lower().replace(" ", "_")


def create_wizard_setup(db: Session, data):

    logger.info("Wizard setup started")

    try:
        # Use transaction block (IMPORTANT)
        with db.begin():

            # -------------------------
            # Pelanggan
            # -------------------------
            pelanggan_kod = generate_kod(data.pelanggan)

            pelanggan = db.query(Pelanggan).filter(
                Pelanggan.kod == pelanggan_kod
            ).first()

            if not pelanggan:
                pelanggan = Pelanggan(
                    kod=pelanggan_kod,
                    nama=data.pelanggan
                )
                db.add(pelanggan)
                db.flush()

            # -------------------------
            # Organisasi (WITH PARENT CHECK)
            # -------------------------
            organisasi_kod = generate_kod(data.organisasi)

            organisasi = db.query(Organisasi).filter(
                Organisasi.kod == organisasi_kod,
                Organisasi.pelanggan_id == pelanggan.id
            ).first()

            if not organisasi:
                organisasi = Organisasi(
                    pelanggan_id=pelanggan.id,
                    kod=organisasi_kod,
                    nama=data.organisasi
                )
                db.add(organisasi)
                db.flush()

            # -------------------------
            # Sub Organisasi (WITH PARENT CHECK)
            # -------------------------
            sub_kod = generate_kod(data.sub_organisasi)

            sub_org = db.query(SubOrganisasi).filter(
                SubOrganisasi.kod == sub_kod,
                SubOrganisasi.organisasi_id == organisasi.id
            ).first()

            if not sub_org:
                sub_org = SubOrganisasi(
                    organisasi_id=organisasi.id,
                    kod=sub_kod,
                    nama=data.sub_organisasi
                )
                db.add(sub_org)
                db.flush()

            # -------------------------
            # Tapak (WITH PARENT CHECK)
            # -------------------------
            tapak_kod = generate_kod(data.tapak)

            tapak = db.query(Tapak).filter(
                Tapak.kod == tapak_kod,
                Tapak.sub_organisasi_id == sub_org.id
            ).first()

            if not tapak:
                tapak = Tapak(
                    sub_organisasi_id=sub_org.id,
                    kod=tapak_kod,
                    nama=data.tapak
                )
                db.add(tapak)
                db.flush()

            # -------------------------
            # Profil (WITH PARENT CHECK)
            # -------------------------
            profil_kod = generate_kod(data.profil)

            profil = db.query(Profil).filter(
                Profil.kod == profil_kod,
                Profil.tapak_id == tapak.id
            ).first()

            if not profil:
                profil = Profil(
                    tapak_id=tapak.id,
                    kod=profil_kod,
                    nama=data.profil
                )
                db.add(profil)
                db.flush()

            # -------------------------
            # Tugasan (Task)
            # -------------------------
            tugasan = Tugasan(
                profil_id=profil.id,
                nama=data.task_name,
                jenis=data.task_type,
                protocol=data.protocol,
                ip_start=str(data.ip_start),
                ip_end=str(data.ip_end)
            )

            db.add(tugasan)
            db.flush()

        # No need for manual commit → handled by db.begin()

        return {
            "message": "Wizard setup completed",
            "pelanggan_id": pelanggan.id,
            "organisasi_id": organisasi.id,
            "sub_organisasi_id": sub_org.id,
            "tapak_id": tapak.id,
            "profil_id": profil.id,
            "tugasan_id": tugasan.id
        }

    except Exception as e:
        logger.error(f"Wizard setup failed: {str(e)}")
        db.rollback()
        raise e