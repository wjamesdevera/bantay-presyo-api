from fastapi import APIRouter
from ..db import SessionDep
from ..services import commodity as commodity_service

router = APIRouter(
    prefix="/commodities",
)


@router.get("/")
def get_commodities(session: SessionDep):
    return commodity_service.get_all_commodities(session)
