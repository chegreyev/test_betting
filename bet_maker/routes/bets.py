from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from models import Bet, BetStatus, BetRequest, BetResponse, ResponseWrapper
from database import get_db
from utils import get_event_status
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/bet",
    response_model=ResponseWrapper[BetResponse],
    status_code=status.HTTP_201_CREATED,
)
async def place_bet(request: BetRequest, db: AsyncSession = Depends(get_db)):
    event = await get_event_status(request.event_id)
    if not event:
        logger.error(f"Event not found: {request.event_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    if event["status"] != "ongoing":
        logger.warning(f"Bets are not allowed on event: {request.event_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bets are not allowed on this event",
        )

    bet = Bet(
        id=str(uuid.uuid4()),
        event_id=request.event_id,
        amount=request.amount,
        status=BetStatus.pending,
    )
    db.add(bet)
    await db.commit()
    await db.refresh(bet)

    logger.info(f"Bet placed successfully: {bet.id}")
    return ResponseWrapper(status="success", data=bet)


@router.get(
    "/bets",
    response_model=ResponseWrapper[List[BetResponse]],
    status_code=status.HTTP_200_OK,
)
async def get_bets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Bet))
    bets_list = result.scalars().all()
    return ResponseWrapper(status="success", data=bets_list)


@router.get(
    "/bets/{bet_id}",
    response_model=ResponseWrapper[BetResponse],
    status_code=status.HTTP_200_OK,
)
async def get_bet(bet_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Bet).where(Bet.id == bet_id))
    bet = result.scalars().first()

    if not bet:
        logger.warning(f"Bet not found: {bet_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bet not found"
        )

    logger.info(f"Bet found: {bet.id}")
    return ResponseWrapper(status="success", data=bet)
