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

from app.services.heartbeat_service import heartbeat

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
        db=db,
        ip_address=request.ip_address,
        tapak_id=request.tapak_id,
        machine_id=request.machine_id,
        hostname=request.hostname,
        profile_id=request.profile_id
    )

@router.get(
    "/{ejen_id}/tugasan",
    response_model=list[AgentTask]
)
def get_tasks(
    ejen_id: int,
    db: Session = Depends(get_db)
):
    heartbeat(
        db=db,
        ejen_id=ejen_id
    )

    return get_tasks_for_agent(
        db,
        ejen_id
    )
