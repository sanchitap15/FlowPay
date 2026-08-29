import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.engine.forecasting import calculate_income_weather
from app.engine.allocation import calculate_flow_allocation
from app.engine.trust_score import compute_trust_score
from app.models import domain
from app.models.schemas import IncomeEventRequest, ProcessIncomeResponse, CreateUserRequest

router = APIRouter(prefix="/api", tags=["income"])


@router.post("/users")
def create_user(payload: CreateUserRequest, db: Session = Depends(get_db)):
    """
    Minimal bootstrap endpoint so the demo can spin up a user before firing
    income events at them. Not meant to be a full auth/signup flow.
    """
    user = domain.User(name=payload.name, income_profile=payload.income_profile)
    db.add(user)
    db.flush()
    db.add(domain.FinancialState(user_id=user.id))
    db.commit()
    db.refresh(user)
    return {"user_id": user.id, "name": user.name, "income_profile": user.income_profile}


@router.post("/process-income", response_model=ProcessIncomeResponse)
def process_income(payload: IncomeEventRequest, db: Session = Depends(get_db)):
    user = db.get(domain.User, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 1. Record the raw income event
    event = domain.IncomeEvent(user_id=user.id, amount=payload.amount, received_at=datetime.utcnow())
    db.add(event)
    db.flush()  # get event.id without committing yet

    # 2. Pull full history to feed the forecasting engine
    past_events = (
        db.query(domain.IncomeEvent)
        .filter(domain.IncomeEvent.user_id == user.id)
        .order_by(domain.IncomeEvent.received_at.asc())
        .all()
    )
    updated_history = [e.amount for e in past_events]

    weather, baseline, forecast_range = calculate_income_weather(updated_history)

    # 3. Determine outstanding loan (sum of active loans)
    active_loans = (
        db.query(domain.Loan)
        .filter(domain.Loan.user_id == user.id, domain.Loan.status == "active")
        .all()
    )
    outstanding_loan = sum(loan.outstanding_balance for loan in active_loans)

    state = db.query(domain.FinancialState).filter(domain.FinancialState.user_id == user.id).first()
    if not state:
        state = domain.FinancialState(user_id=user.id)
        db.add(state)
        db.flush()

    savings_goal_met = False  # placeholder hook â wire to SavingsPocket goals when that flow exists
    allocation = calculate_flow_allocation(payload.amount, weather, outstanding_loan, savings_goal_met)

    # 4. Apply repayment against the loan ledger
    repay_amt = allocation["allocations"]["repayment"]
    remaining_repay = repay_amt
    for loan in active_loans:
        if remaining_repay <= 0:
            break
        applied = min(loan.outstanding_balance, remaining_repay)
        loan.outstanding_balance -= applied
        remaining_repay -= applied
        if loan.outstanding_balance <= 0:
            loan.status = "closed"

    # 5. Track shock -> recovery transitions correctly (recovery = leaving a shock, not being in one)
    if weather == "SHOCK":
        state.shock_streak = True
    elif weather in ("STABLE", "STRONG") and state.shock_streak:
        state.shocks_recovered += 1
        state.shock_streak = False

    state.baseline_income = baseline
    state.forecast_low, state.forecast_high = forecast_range
    state.weather_status = weather
    state.savings_active = allocation["allocations"]["savings"] > 0
    state.updated_at = datetime.utcnow()

    # 6. Persist this allocation for audit trail + explainability history
    allocation_row = domain.Allocation(
        user_id=user.id,
        income_event_id=event.id,
        spendable=allocation["allocations"]["spendable"],
        savings=allocation["allocations"]["savings"],
        repayment=allocation["allocations"]["repayment"],
        protected=allocation["allocations"]["protected"],
        weather_status=weather,
        repayment_due=outstanding_loan > 0,
        explanation=allocation["explanation"],
    )
    db.add(allocation_row)

    # 7. Recompute trust score from real allocation history (not hardcoded)
    past_allocations = (
        db.query(domain.Allocation)
        .filter(domain.Allocation.user_id == user.id)
        .order_by(domain.Allocation.created_at.asc())
        .all()
    )
    repayment_log = [
        {"repayment_due": a.repayment_due, "repayment": a.repayment} for a in past_allocations
    ]
    missed_repayments = sum(
        1 for a in past_allocations if a.repayment_due and a.repayment == 0
    )

    trust = compute_trust_score(
        history=repayment_log,
        savings_active=state.savings_active,
        shocks_handled=state.shocks_recovered,
        volatility_increased=(weather in ("LEAN", "SHOCK")),
        missed_repayments=missed_repayments,
    )

    trust_row = domain.TrustScoreHistory(
        user_id=user.id,
        score=trust["score"],
        factors_json=json.dumps(trust["factors"]),
    )
    db.add(trust_row)

    db.commit()

    return {
        "weather": weather,
        "baseline": baseline,
        "forecast_range": forecast_range,
        "allocation": allocation,
        "trust_score": trust,
        "updated_history": updated_history,
    }