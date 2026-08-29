from typing import Dict, Any, List


def compute_trust_score(
    history: List[Dict[str, Any]],
    savings_active: bool,
    shocks_handled: int,
    volatility_increased: bool = False,
    missed_repayments: int = 0,
) -> Dict[str, Any]:
    """
    Computes an explainable 0-100 dynamic trust score based on behavioral factors.

    `history` entries are expected to look like:
        {"repayment_due": bool/int, "repayment": float}
    """
    base_score = 65
    factors = []

    # Only count entries where a repayment was actually due AND was paid
    successful_repayments = sum(
        1 for h in history if h.get("repayment_due", 0) and h.get("repayment", 0) > 0
    )
    if successful_repayments >= 5:
        base_score += 12
        factors.append({"label": "Consistent Repayments", "impact": "+12"})

    if savings_active:
        base_score += 8
        factors.append({"label": "Maintained Emergency Buffer", "impact": "+8"})

    if shocks_handled > 0:
        base_score += 5
        factors.append({"label": "Recovered from Income Shock", "impact": "+5"})

    # --- Negative factors ---
    if missed_repayments > 0:
        penalty = min(missed_repayments * 4, 20)  # capped so one bad stretch doesn't zero the score
        base_score -= penalty
        factors.append({"label": "Missed Repayments", "impact": f"-{penalty}"})

    if volatility_increased:
        base_score -= 2
        factors.append({"label": "Increased Income Volatility", "impact": "-2"})

    final_score = max(0, min(100, base_score))

    return {
        "score": final_score,
        "factors": factors,
    }