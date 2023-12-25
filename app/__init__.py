import traceback
from http.client import INTERNAL_SERVER_ERROR

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import Base, engine
from app.utils.constants import CRYPTO_DECIMALS

from .routes import router

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(Exception)
async def internal_server_error_handler(_: Request, exc: Exception):
    traceback_info = traceback.extract_tb(exc.__traceback__)
    filename, line = traceback_info[-1][0], traceback_info[-1][1]
    msg = str(exc)
    exc_type = type(exc).__name__
    return JSONResponse(status_code=INTERNAL_SERVER_ERROR, content={"detail": {
        "loc": [filename, line],
        "msg": msg,
        "type": exc_type
    }})

app.include_router(router)
