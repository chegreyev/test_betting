from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Event(BaseModel):
    event_id: str  
    odds: float = Field(..., gt=0)  
    deadline: datetime  
    status: str = "ongoing"


class EventStorage:
    events: Dict[str, Event] = {}

    @classmethod
    def add_event(cls, event: Event) -> None:
        cls.events[event.event_id] = event

    @classmethod
    def get_event(cls, event_id: str) -> Optional[Event]:
        return cls.events.get(event_id)

    @classmethod
    def get_available_events(cls) -> List[Event]:
        return [e for e in cls.events.values() if e.status == "ongoing"]
