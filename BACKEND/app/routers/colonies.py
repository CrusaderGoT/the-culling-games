from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select, func

from ..models.player import Player

from ..utils.config import Tag
from ..utils.dependencies import session
from ..auth.dependencies import oauth2_scheme
from ..models.colony import Colony, ColonyInfo

# write you match api routes here

router = APIRouter(
    prefix="/colony", tags=[Tag.colony], dependencies=[Depends(oauth2_scheme)]
)


@router.get("/all", response_model=list[ColonyInfo])
def get_matches(
    session: session,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=30)] = 10,
):
    "get all matches"
    stmt = (
        select(Colony)
        .join(Colony.players)
        .group_by(Colony.id)
        .order_by(func.max(Player.points).desc())
        .offset(offset)
        .limit(limit)
    )
    result = session.exec(stmt).all()
    if result:
        return result
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No colony yet...")
