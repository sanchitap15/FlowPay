from typing import Dict, Any

# Base target allocation ratios per Income Weather state.
# Each state's values sum to 1.0 (spend + save + repay + protect).
RATIOS = {
    "STRONG": {"save": 0.15, "repay": 0.10, "protect": 0.0, "spend": 0.75},
    "STABLE": {"save": 0.10, "repay": 0.07, "protect": 0.0, "spend": 0.83},
    "LEAN":   {"save": 0.03, "repay": 0.02, "protect": 0.30, "spend": 0.65},
    "SHOCK":  {"save": 0.01, "repay": 0.01, "protect": 0.50, "spend": 0.48},
}


def calculate_flow_allocation(
    income_amount: float,
    weather: str,
    outstanding_loan: float,
    savings_goal_met: bool = False,
) -> Dict[str, Any]:
    """
    Constrained Rule-Based Optimization Engine.
    Adjusts split dynamically based on detected Income Weather.
    """
    selected = RATIOS.get(weather, RATIOS["STABLE"])

    # Clamp so a bad/negative outstanding_loan value can never produce a negative repayment
    safe_outstanding_loan = max(outstanding_loan, 0.0)

    # Do not allocate to loan if balance is zero (or already cleared)
    repay_ratio = selected["repay"] if safe_outstanding_loan > 0 else 0.0

    # If the user's savings goal is already met, redirect that ratio to spendable
    save_ratio = 0.0 if savings_goal_met else selected["save"]
    protect_ratio = selected["protect"]

    save_amt = round(income_amount * save_ratio, 2)
    repay_amt = round(min(income_amount * repay_ratio, safe_outstanding_loan), 2)
    protect_amt = round(income_amount * protect_ratio, 2)
    # spend_amt derived by subtraction so rounding error is absorbed here, not elsewhere
    spend_amt = round(income_amount - (save_amt + repay_amt + protect_amt), 2)

    if savings_goal_met and weather in ("STRONG", "STABLE"):
        explanation_map = {
            "STRONG": f"Savings goal already met â extra kept spendable. â¹{repay_amt} paid toward credit.",
            "STABLE": f"Savings goal already met â extra kept spendable. â¹{repay_amt} paid toward credit.",
        }
    else:
        explanation_map = {
            "STRONG": f"Income is high. Safe to save â¹{save_amt} and pay â¹{repay_amt} toward credit.",
            "STABLE": f"Normal earning pattern detected. Saved â¹{save_amt} and allocated â¹{repay_amt} to credit.",
            "LEAN": f"Earnings are below normal. Savings reduced to â¹{save_amt}; â¹{protect_amt} protected for essentials.",
            "SHOCK": f"Income shock detected! Repayment reduced to â¹{repay_amt} to preserve core liquidity.",
        }

    return {
        "income_amount": income_amount,
        "weather": weather,
        "allocations": {
            "spendable": spend_amt,
            "savings": save_amt,
            "repayment": repay_amt,
            "protected": protect_amt,
        },
        "explanation": explanation_map.get(weather, "Standard allocation applied."),
    }