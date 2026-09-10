from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging_config import setup_logging
from app.core.exceptions import register_exception_handlers
from app.core.middleware import RequestContextMiddleware, SimpleRateLimitMiddleware
from app.core.scheduler import start_scheduler, stop_scheduler
from app.api import (
    routes_income,
    routes_allocation,
    routes_trust,
    routes_demo,
    routes_auth,
    routes_export,
    routes_health,
)

setup_logging()

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield
    # Shutdown
    stop_scheduler()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SimpleRateLimitMiddleware, max_requests=60, window_seconds=60)
app.add_middleware(RequestContextMiddleware)

register_exception_handlers(app)

app.include_router(routes_income.router)
app.include_router(routes_allocation.router)
app.include_router(routes_trust.router)
app.include_router(routes_demo.router)
app.include_router(routes_auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(routes_export.router, prefix="/api/export", tags=["export"])
app.include_router(routes_health.router, tags=["health"])