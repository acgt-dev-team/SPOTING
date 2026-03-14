from sqlalchemy.orm import Session

from app.models.pelanggan import Pelanggan
from app.models.organisasi import Organisasi
from app.models.sub_organisasi import SubOrganisasi
from app.models.tapak import Tapak
from app.models.profil import Profil
from app.models.tugasan import Tugasan


def create_wizard_setup(db: Session, data):

    try:

        pelanggan_kod = data.pelanggan.lower().replace(" ", "_")

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

        organisasi_kod = data.organisasi.lower().replace(" ", "_")

        organisasi = db.query(Organisasi).filter(
            Organisasi.kod == organisasi_kod
        ).first()

        if not organisasi:
            organisasi = Organisasi(
                pelanggan_id=pelanggan.id,
                kod=organisasi_kod,
                nama=data.organisasi
            )
            db.add(organisasi)
            db.flush()

        sub_kod = data.sub_organisasi.lower().replace(" ", "_")

        sub_org = db.query(SubOrganisasi).filter(
            SubOrganisasi.kod == sub_kod
        ).first()

        if not sub_org:
            sub_org = SubOrganisasi(
                organisasi_id=organisasi.id,
                kod=sub_kod,
                nama=data.sub_organisasi
            )
            db.add(sub_org)
            db.flush()

        tapak_kod = data.tapak.lower().replace(" ", "_")

        tapak = db.query(Tapak).filter(
            Tapak.kod == tapak_kod
        ).first()

        if not tapak:
            tapak = Tapak(
                sub_organisasi_id=sub_org.id,
                kod=tapak_kod,
                nama=data.tapak
            )
            db.add(tapak)
            db.flush()

        profil_kod = data.profil.lower().replace(" ", "_")

        profil = db.query(Profil).filter(
            Profil.kod == profil_kod
        ).first()

        if not profil:
            profil = Profil(
                tapak_id=tapak.id,
                kod=profil_kod,
                nama=data.profil
            )
            db.add(profil)
            db.flush()

        tugasan = Tugasan(
            profil_id=profil.id,
            nama=data.task_name,
            jenis=data.task_type,
            protocol=data.protocol,
            ip_start=data.ip_start,
            ip_end=data.ip_end
        )

        db.add(tugasan)

        db.commit()

        return {
            "message": "Wizard setup completed"
        }

    except Exception as e:

        db.rollback()

        raise e