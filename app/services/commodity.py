from sqlmodel import select
from app.models import Commodity
from app.db import SessionDep


def get_all_commodities(session: SessionDep):
    return session.exec(select(Commodity).limit(20)).all()
