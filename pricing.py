"""Pricing rules and fee calculations for ATA Martial Arts."""

WEEKS = 4
COACH_RATE = 9.50
COMP_FEE = 22.00
MAX_COACH_HOURS = 5
# Sanity limit, not a client rule: the brief sets no maximum.
MAX_COMPETITIONS = 5

WEEKLY_FEES = {
    "Beginner": 25.00,
    "Intermediate": 30.00,
    "Elite": 35.00,
}

# Upper limit is in kg. None means no limit (Heavyweight is over 100 kg).
WEIGHT_CATEGORIES = [
    ("Flyweight", 66),
    ("Lightweight", 73),
    ("Light-Middleweight", 81),
    ("Middleweight", 90),
    ("Light-Heavyweight", 100),
    ("Heavyweight", None),
]


def training_cost(plan: str) -> float:
    """Return the monthly training cost for the given plan."""
    return WEEKLY_FEES[plan] * WEEKS


def coaching_cost(hours_per_week: float) -> float:
    """Return the monthly coaching cost from hours entered per week."""
    return hours_per_week * COACH_RATE * WEEKS


def competition_cost(number: int) -> float:
    """Return the cost of entering the given number of competitions."""
    return number * COMP_FEE


def monthly_total(
    plan: str, hours_per_week: float, competitions: int
) -> float:
    """Return the monthly total in pounds, rounded to 2 decimal places."""
    total = (
        training_cost(plan)
        + coaching_cost(hours_per_week)
        + competition_cost(competitions)
    )
    return round(total, 2)
