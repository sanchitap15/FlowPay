from typing import List, Tuple

from app.engine.shock_detector import (
    compute_baseline_and_ratio,
    compute_volatility_spread,
    classify_weather,
)


def calculate_income_weather(recent_earnings: List[float]) -> Tuple[str, float, Tuple[float, float]]:
    """
    Calculates moving baseline, forecasts next 7-day range, and sets Weather status.
    Returns (weather_label, baseline, (forecast_low, forecast_high)).
    """
    if not recent_earnings:
        return "STABLE", 0.0, (0.0, 0.0)

    if len(recent_earnings) == 1:
        # Not enough history to detect a trend or shock yet — treat as stable
        val = recent_earnings[0]
        return "STABLE", val, (round(val * 0.85, -1), round(val * 1.15, -1))

    baseline, ratio = compute_baseline_and_ratio(recent_earnings)
    spread = compute_volatility_spread(recent_earnings)

    latest_avg_window = recent_earnings[-3:]
    latest_avg = sum(latest_avg_window) / len(latest_avg_window)

    # Exponential smoothing forecast
    alpha = 0.3
    forecast_base = alpha * latest_avg + (1 - alpha) * baseline

    lower_bound = round(forecast_base * (1 - spread), -1)
    upper_bound = round(forecast_base * (1 + spread), -1)

    weather = classify_weather(ratio)

    return weather, baseline, (lower_bound, upper_bound)