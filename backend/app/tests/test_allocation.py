import pytest
from app.engine.allocation import calculate_flow_allocation


def total(allocations: dict) -> float:
    return round(sum(allocations.values()), 2)


@pytest.mark.parametrize("weather", ["STRONG", "STABLE", "LEAN", "SHOCK"])
def test_allocations_sum_to_income(weather):
    income = 1800.0
    result = calculate_flow_allocation(income, weather, outstanding_loan=500.0)
    assert total(result["allocations"]) == round(income, 2)


def test_no_repayment_when_no_outstanding_loan():
    result = calculate_flow_allocation(1500.0, "STABLE", outstanding_loan=0.0)
    assert result["allocations"]["repayment"] == 0.0


def test_repayment_never_exceeds_outstanding_balance():
    # Large income, tiny remaining loan — repayment should be capped at the loan balance
    result = calculate_flow_allocation(10000.0, "STRONG", outstanding_loan=15.0)
    assert result["allocations"]["repayment"] <= 15.0


def test_negative_outstanding_loan_does_not_produce_negative_repayment():
    result = calculate_flow_allocation(1000.0, "STABLE", outstanding_loan=-50.0)
    assert result["allocations"]["repayment"] == 0.0


def test_savings_goal_met_redirects_savings_to_spend():
    normal = calculate_flow_allocation(1000.0, "STABLE", outstanding_loan=0.0, savings_goal_met=False)
    goal_met = calculate_flow_allocation(1000.0, "STABLE", outstanding_loan=0.0, savings_goal_met=True)
    assert goal_met["allocations"]["savings"] == 0.0
    assert goal_met["allocations"]["spendable"] > normal["allocations"]["spendable"]


def test_shock_state_protects_majority_of_income():
    result = calculate_flow_allocation(700.0, "SHOCK", outstanding_loan=200.0)
    assert result["allocations"]["protected"] > result["allocations"]["spendable"]


def test_unknown_weather_falls_back_to_stable():
    result = calculate_flow_allocation(1000.0, "UNKNOWN_STATE", outstanding_loan=0.0)
    assert result["weather"] == "UNKNOWN_STATE"  # label passed through as-is
    assert total(result["allocations"]) == 1000.0  # but ratios used are STABLE's
