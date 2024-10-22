import httpx
from fastapi import HTTPException
from config import settings


async def get_event_status(event_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.LINE_PROVIDER_URL}/events/{event_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Event not found")
        return response.json().get("data")
