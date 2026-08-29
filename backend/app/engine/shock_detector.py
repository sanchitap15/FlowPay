from typing import List, Tuple
import numpy as np

from app.core.config import get_settings

settings = get_settings()


def compute_baseline_and_ratio(recent_earnings: List[float]) -> Tuple[float, float]:
    """
    Builds a baseline from history EXCLUDING the most recent point(s), then
    returns (baseline, ratio) where ratio compares a smoothed "latest" window
    against that baseline.

    Excluding the latest point from the baseline matters: if you fold a big
    drop into the very average you're comparing it against, the drop drags
    the baseline down with it and the shock signal gets diluted.
    """
    if len(recent_earnings) < 2:
        val = recent_earnings[0] if recent_earnings else 0.0
        return val, 1.0

    history = recent_earnings[:-1]
    baseline = float(np.mean(history[-14:])) if len(history) >= 14 else float(np.mean(history))

    # Average of last up to 3 points, not just the single latest, to reduce noise
    # from one outlier day swinging the whole weather status.
    recent_window = recent_earnings[-3:]
    latest_avg = float(np.mean(recent_window))

    ratio = latest_avg / baseline if baseline > 0 else 1.0
    return baseline, ratio


def compute_volatility_spread(recent_earnings: List[float]) -> float:
    """
    Coefficient of variation, clamped to a sane range, used to widen or
    narrow the forecast band instead of a fixed +/-15% for every user.
    """
    if len(recent_earnings) < 3:
        return settings.FORECAST_MIN_SPREAD

    history = recent_earnings[:-1] if len(recent_earnings) >= 2 else recent_earnings
    window = history[-14:]
    mean_val = float(np.mean(window))
    std_val = float(np.std(window))

    cv = std_val / mean_val if mean_val > 0 else 0.0
    return min(max(cv, settings.FORECAST_MIN_SPREAD), settings.FORECAST_MAX_SPREAD)


def classify_weather(ratio: float) -> str:
    """
    Pure classification function â kept separate from the numeric baseline
    logic above so it's trivially unit-testable with hand-picked ratios.
    """
    if ratio < settings.SHOCK_RATIO_THRESHOLD:
        return "SHOCK"
    elif ratio < settings.LEAN_RATIO_THRESHOLD:
        return "LEAN"
    elif ratio > settings.STRONG_RATIO_THRESHOLD:
        return "STRONG"
    else:
        return "STABLE"