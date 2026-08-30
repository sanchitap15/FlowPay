from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import domain

router = APIRouter(prefix="/api", tags=["allocation"])


@router.get("/allocation/{user_id}/latest")
def get_latest_allocation(user_id: str, db: Session = Depends(get_db)):
    user = db.get(domain.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    latest = (
        db.query(domain.Allocation)
        .filter(domain.Allocation.user_id == user_id)
        .order_by(domain.Allocation.created_at.desc())
        .first()
    )
    if not latest:
        raise HTTPException(status_code=404, detail="No allocations yet for this user")

    return {
        "weather": latest.weather_status,
        "allocations": {
            "spendable": latest.spendable,
            "savings": latest.savings,
            "repayment": latest.repayment,
            "protected": latest.protected,
        },
        "explanation": latest.explanation,
        "created_at": latest.created_at.isoformat(),
    }


@router.get("/allocation/{user_id}/history")
def get_allocation_history(user_id: str, limit: int = 30, db: Session = Depends(get_db)):
    user = db.get(domain.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    rows = (
        db.query(domain.Allocation)
        .filter(domain.Allocation.user_id == user_id)
        .order_by(domain.Allocation.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "weather": r.weather_status,
            "spendable": r.spendable,
            "savings": r.savings,
            "repayment": r.repayment,
            "protected": r.protected,
            "explanation": r.explanation,
            "created_at": r.created_at.isoformat(),
        }
        for r in reversed(rows)  # oldest -> newest, easier for frontend timeline charts
    ]
