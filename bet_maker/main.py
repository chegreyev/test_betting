from fastapi.exceptions import RequestValidationError
from routes.bets import router as bets_router
from database import init_db

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from models import ResponseWrapper

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(bets_router, tags=["bets"])


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseWrapper(status="error", error=exc.detail).dict(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=ResponseWrapper(status="error", error=str(exc)).dict(),
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content=ResponseWrapper(status="error", error="Database error").dict(),
    )


@app.get("/health")
async def health_check():
    return {"status": "success", "data": {"message": "Service is healthy"}}
