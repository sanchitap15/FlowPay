import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import domain

router = APIRouter(prefix="/api", tags=["trust"])


@router.get("/trust/{user_id}/latest")
def get_latest_trust_score(user_id: str, db: Session = Depends(get_db)):
    user = db.get(domain.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    latest = (
        db.query(domain.TrustScoreHistory)
        .filter(domain.TrustScoreHistory.user_id == user_id)
        .order_by(domain.TrustScoreHistory.created_at.desc())
        .first()
    )
    if not latest:
        # New user with no history yet — return the neutral base score, not an error,
        # so the dashboard doesn't have to special-case a 404 on first load.
        return {"score": 65, "factors": []}

    return {"score": latest.score, "factors": json.loads(latest.factors_json)}


@router.get("/trust/{user_id}/history")
def get_trust_history(user_id: str, limit: int = 30, db: Session = Depends(get_db)):
    user = db.get(domain.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    rows = (
        db.query(domain.TrustScoreHistory)
        .filter(domain.TrustScoreHistory.user_id == user_id)
        .order_by(domain.TrustScoreHistory.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "score": r.score,
            "factors": json.loads(r.factors_json),
            "created_at": r.created_at.isoformat(),
        }
        for r in reversed(rows)
    ]