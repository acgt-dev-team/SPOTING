from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.ejen import (
    EjenRegister,
    EjenResponse,
)

from app.services.agent_service import get_tasks_for_agent

from app.schemas.agent_task import AgentTask

from app.services.ejen_service import register_ejen
from app.i18n import t

router = APIRouter(
    prefix="/ejen",
    tags=[t("docs.tags.agent")]
)


@router.post(
    "/register",
    response_model=EjenResponse
)
def register(
    request: EjenRegister,
    db: Session = Depends(get_db)
):
    return register_ejen(
        db,
        request.ip_address,
        request.tapak_id
    )

@router.get(
    "/{ejen_id}/tugasan",
    response_model=list[AgentTask]
)
def get_tasks(
    ejen_id: int,
    db: Session = Depends(get_db)
):
    return get_tasks_for_agent(
        db,
        ejen_id
    )
