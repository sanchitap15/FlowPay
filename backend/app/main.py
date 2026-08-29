from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api import routes_income, routes_allocation, routes_trust, routes_demo

settings = get_settings()

app = FastAPI(title=settings.APP_NAME)

# NOTE: allow_credentials=True cannot be combined with allow_origins=["*"] —
# browsers reject that combination outright. List real origins explicitly instead.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_income.router)
app.include_router(routes_allocation.router)
app.include_router(routes_trust.router)
app.include_router(routes_demo.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "environment": settings.ENVIRONMENT}