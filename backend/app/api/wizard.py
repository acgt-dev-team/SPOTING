from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.wizard_schema import WizardSetup
from app.services.wizard_service import create_wizard_setup

router = APIRouter(
    prefix="/api/wizard",
    tags=["Wizard"]
)


@router.post("/setup")
def wizard_setup(
    data: WizardSetup,
    db: Session = Depends(get_db)
):

    result = create_wizard_setup(db, data)

    return result