from fastapi import FastAPI, HTTPException
import redis
import orjson
from datetime import datetime

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from models import Event

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code, content={"status": "error", "data": None}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "data": exc.errors(),  
        },
    )


@app.get("/health")
async def health_check():
    return {"status": "success", "data": {"message": "Service is healthy"}}


redis_client = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=True)


@app.post("/events")
async def create_event(event: Event):
    event_data = event.dict()
    redis_client.set(event.event_id, orjson.dumps(event_data).decode())
    return {"status": "success", "data": event_data}


@app.get("/events/{event_id}")
async def get_event(event_id: str):
    event = redis_client.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event_data = orjson.loads(event)
    return {"status": "success", "data": event_data}


@app.get("/events")
async def get_events():
    keys = redis_client.keys()
    events = [orjson.loads(redis_client.get(key)) for key in keys]
    available_events = [event for event in events if event["status"] == "ongoing"]
    return {"status": "success", "data": available_events}
