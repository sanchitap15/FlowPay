from typing import List, Optional, Tuple
from pydantic import BaseModel, Field


# ---------- Requests ----------

class IncomeEventRequest(BaseModel):
    user_id: str
    amount: float = Field(gt=0, description="Income amount must be positive")


class CreateUserRequest(BaseModel):
    name: str
    income_profile: str = "delivery_worker"


class DemoShockRequest(BaseModel):
    user_id: str
    num_events: int = Field(default=3, ge=1, le=10)


class DemoResetRequest(BaseModel):
    user_id: str


# ---------- Responses ----------

class AllocationBreakdown(BaseModel):
    spendable: float
    savings: float
    repayment: float
    protected: float


class AllocationResponse(BaseModel):
    income_amount: float
    weather: str
    allocations: AllocationBreakdown
    explanation: str


class TrustFactor(BaseModel):
    label: str
    impact: str


class TrustScoreResponse(BaseModel):
    score: int
    factors: List[TrustFactor]


class ProcessIncomeResponse(BaseModel):
    weather: str
    baseline: float
    forecast_range: Tuple[float, float]
    allocation: AllocationResponse
    trust_score: TrustScoreResponse
    updated_history: List[float]


class TrustHistoryEntry(BaseModel):
    score: int
    factors: List[TrustFactor]
    created_at: str