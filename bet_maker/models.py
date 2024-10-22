from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Generic, TypeVar, Optional
from pydantic.generics import GenericModel
from enum import Enum as PyEnum
from uuid import UUID
import uuid

Base = declarative_base()


class BetStatus(str, PyEnum):
    pending = "pending"
    won = "won"
    lost = "lost"


class Bet(Base):
    __tablename__ = "bets"

    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(
        SQLAlchemyEnum(BetStatus), default=BetStatus.pending, nullable=False
    )


class BetRequest(BaseModel):
    event_id: str
    amount: float = Field(..., gt=0)

    model_config = ConfigDict(
        from_attributes=True,
    )


class BetResponse(BaseModel):
    id: UUID
    event_id: str
    amount: float
    status: BetStatus

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


DataT = TypeVar("DataT")


class ResponseWrapper(GenericModel, Generic[DataT]):
    status: str
    data: Optional[DataT] = None
    error: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
