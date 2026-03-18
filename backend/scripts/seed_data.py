from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.pelanggan import Pelanggan

db: Session = SessionLocal()

if not db.query(Pelanggan).first():
    pelanggan = Pelanggan(
        kod="default_customer",
        nama="Default Customer"
    )

    db.add(pelanggan)
    db.commit()

print("Seed data inserted")
