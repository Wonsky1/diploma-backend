import logging

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.routers import robot_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log")],
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Listkit API",
    version=settings.API_VERSION,
    lifespan=lifespan,
    contact={
        "name": "API Support",
        "email": "vladyslav.pidborskyi@gmail.com",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    summary="API Root",
    description="Returns basic information about the API",
    tags=["General"],
)
async def root():
    return {
        "message": "API is running",
    }

# Register all routers
app.include_router(robot_router)

