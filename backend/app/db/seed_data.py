"""
Generates synthetic 60-90 day income histories for the four profiles
mentioned in the pitch deck. Not real UPI data — explicitly simulated,
as the deck states.

Run:
    python -m app.db.seed_data
"""
import random
from typing import List

random.seed(42)  # deterministic output so demo runs are reproducible


def generate_delivery_worker(days: int = 60) -> List[float]:
    """Daily volatile earnings, occasional zero-income days."""
    earnings = []
    for _ in range(days):
        if random.random() < 0.08:
            earnings.append(0.0)
        else:
            earnings.append(round(random.uniform(600, 2400), -1))
    return earnings


def generate_driver(days: int = 60) -> List[float]:
    """Weekday/weekend variation — weekends earn more."""
    earnings = []
    for day in range(days):
        is_weekend = day % 7 in (5, 6)
        base = random.uniform(1400, 2600) if is_weekend else random.uniform(800, 1600)
        earnings.append(round(base, -1))
    return earnings


def generate_vendor(days: int = 60) -> List[float]:
    """Highly variable cash flow, some very low days mixed with spikes."""
    earnings = []
    for _ in range(days):
        roll = random.random()
        if roll < 0.15:
            earnings.append(round(random.uniform(0, 300), -1))
        elif roll > 0.9:
            earnings.append(round(random.uniform(3000, 5000), -1))
        else:
            earnings.append(round(random.uniform(500, 1800), -1))
    return earnings


def generate_farmer(days: int = 90) -> List[float]:
    """Strongly seasonal — long stretches near zero, then harvest spikes."""
    earnings = []
    harvest_windows = {20, 21, 22, 55, 56, 57, 58}
    for day in range(days):
        if day in harvest_windows:
            earnings.append(round(random.uniform(15000, 40000), -1))
        else:
            earnings.append(round(random.uniform(0, 200), -1))
    return earnings


def inject_shock_and_recovery(earnings: List[float]) -> List[float]:
    """
    Appends a scripted shock -> recovery tail onto any profile, for the
    live demo's 'SIMULATE INCOME SHOCK' / 'SIMULATE RECOVERY' buttons.
    """
    shock = [300.0, 450.0, 250.0]
    recovery = [1600.0, 2200.0]
    return earnings + shock + recovery


PROFILE_GENERATORS = {
    "delivery_worker": generate_delivery_worker,
    "driver": generate_driver,
    "vendor": generate_vendor,
    "farmer": generate_farmer,
}


if __name__ == "__main__":
    for name, generator in PROFILE_GENERATORS.items():
        sample = generator()
        print(f"{name}: {len(sample)} days, first 5 = {sample[:5]}")
