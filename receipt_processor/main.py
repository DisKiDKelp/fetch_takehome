from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .routes import get_points, process


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan of the web app function."""

    # initalize receipt store for easy access
    app.state.reciept_hashs = {}
    app.state.reciept_ids = {}

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(get_points.router)
app.include_router(process.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(*args, **kwargs):
    # Custom Error handling encase of validation errors on receipt input
    return JSONResponse(status_code=400, content="The receipt is invalid.")
