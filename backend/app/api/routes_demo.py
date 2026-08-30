from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.routes_income import process_income
from app.models import domain
from app.models.schemas import IncomeEventRequest, DemoResetRequest

router = APIRouter(prefix="/api/demo", tags=["demo"])

# Scripted sequences matching section 12 of the pitch deck's live demo walkthrough
SHOCK_SEQUENCE = [300.0, 450.0, 250.0]
RECOVERY_SEQUENCE = [1600.0, 2200.0]


@router.post("/simulate-shock/{user_id}")
def simulate_shock(user_id: str, db: Session = Depends(get_db)):
    user = db.get(domain.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    results = []
    for amount in SHOCK_SEQUENCE:
        result = process_income(IncomeEventRequest(user_id=user_id, amount=amount), db=db)
        results.append(result)

    return {"sequence": "shock", "steps": results}


@router.post("/simulate-recovery/{user_id}")
def simulate_recovery(user_id: str, db: Session = Depends(get_db)):
    user = db.get(domain.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    results = []
    for amount in RECOVERY_SEQUENCE:
        result = process_income(IncomeEventRequest(user_id=user_id, amount=amount), db=db)
        results.append(result)

    return {"sequence": "recovery", "steps": results}


@router.post("/reset")
def reset_demo_user(payload: DemoResetRequest, db: Session = Depends(get_db)):
    """
    Wipes a demo user's income/allocation/trust history and resets their
    financial state, without deleting the user itself — lets you re-run the
    pitch demo from a clean slate between practice runs.
    """
    user = db.get(domain.User, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(domain.Allocation).filter(domain.Allocation.user_id == user.id).delete()
    db.query(domain.TrustScoreHistory).filter(domain.TrustScoreHistory.user_id == user.id).delete()
    db.query(domain.IncomeEvent).filter(domain.IncomeEvent.user_id == user.id).delete()
    db.query(domain.Loan).filter(domain.Loan.user_id == user.id).delete()

    state = db.query(domain.FinancialState).filter(domain.FinancialState.user_id == user.id).first()
    if state:
        state.baseline_income = 0.0
        state.forecast_low = 0.0
        state.forecast_high = 0.0
        state.weather_status = "STABLE"
        state.shock_streak = False
        state.shocks_recovered = 0
        state.savings_active = False

    db.commit()
    return {"status": "reset", "user_id": user.id}
