from app.engine.shock_detector import classify_weather, compute_baseline_and_ratio
from app.engine.forecasting import calculate_income_weather


def test_classify_weather_boundaries():
    assert classify_weather(0.40) == "SHOCK"
    assert classify_weather(0.70) == "LEAN"
    assert classify_weather(1.00) == "STABLE"
    assert classify_weather(1.30) == "STRONG"


def test_empty_history_returns_stable_default():
    weather, baseline, forecast = calculate_income_weather([])
    assert weather == "STABLE"
    assert baseline == 0.0
    assert forecast == (0.0, 0.0)


def test_single_data_point_is_treated_as_stable():
    weather, baseline, forecast = calculate_income_weather([1000.0])
    assert weather == "STABLE"
    assert baseline == 1000.0


def test_baseline_excludes_the_latest_point():
    # History of steady 1000s, then one big drop to 100.
    # Baseline should reflect the steady period, NOT be dragged down by the drop itself.
    history = [1000.0] * 10 + [100.0]
    baseline, ratio = compute_baseline_and_ratio(history)
    # Baseline should stay anchored near the steady 1000 period, not get pulled
    # down toward 100 just because the drop is in the window.
    assert baseline > 900
    # Ratio uses an average of the last 3 points (two 1000s + one 100), so it
    # won't be as extreme as 100/1000, but it should still clearly show a dip.
    assert ratio < 0.8


def test_sustained_drop_triggers_shock_classification():
    history = [1000.0] * 10 + [900.0, 850.0, 200.0]
    weather, _, _ = calculate_income_weather(history)
    assert weather in ("SHOCK", "LEAN")  # last-3 average pulls the ratio down meaningfully


def test_single_outlier_day_does_not_alone_trigger_shock():
    # One bad day surrounded by otherwise strong recent earnings shouldn't,
    # on its own, swing the whole status to SHOCK — averaging the last 3
    # smooths this out.
    history = [1000.0] * 10 + [1100.0, 0.0, 1050.0]
    weather, _, _ = calculate_income_weather(history)
    assert weather != "SHOCK"


def test_forecast_bounds_are_ordered():
    history = [800.0, 950.0, 700.0, 1100.0, 600.0, 1200.0, 500.0]
    _, _, (low, high) = calculate_income_weather(history)
    assert low <= high
