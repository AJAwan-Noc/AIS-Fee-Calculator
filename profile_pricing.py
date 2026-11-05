"""Used with cProfile to check performance of the fee calculations.

Run with: python -m cProfile -s cumulative profile_pricing.py
"""

from athlete import Athlete, Squad
from pricing import MAX_COMPETITIONS, WEEKLY_FEES

ATHLETE_COUNT = 20000
COACHING_HOURS = [0, 2, 5]
# Example weight and category; they do not affect the fee.
SAMPLE_WEIGHT = 70.0
SAMPLE_CATEGORY = "Lightweight"


def build_athlete(number: int, plans: list) -> Athlete:
    """Build one athlete, mixing plan, coaching hours and competitions."""
    plan = plans[number % len(plans)]
    # Dividing first makes each value change at a different rate, so the
    # athletes cover many different combinations.
    hours = COACHING_HOURS[(number // 3) % len(COACHING_HOURS)]
    competitions = (number // 9) % (MAX_COMPETITIONS + 1)
    if plan == "Beginner":
        competitions = 0
    name = "Athlete " + str(number + 1)
    return Athlete(
        name, plan, SAMPLE_WEIGHT, SAMPLE_CATEGORY, competitions, hours
    )


def build_squad() -> Squad:
    """Build a squad of ATHLETE_COUNT athletes."""
    squad = Squad()
    plans = list(WEEKLY_FEES)
    for number in range(ATHLETE_COUNT):
        squad.add_athlete(build_athlete(number, plans))
    return squad


def add_up_totals(squad: Squad) -> float:
    """Call monthly_breakdown() on every athlete and add up the totals."""
    grand_total = 0.0
    for athlete in squad.get_all():
        lines, total = athlete.monthly_breakdown()
        grand_total = grand_total + total
    return grand_total


def main() -> None:
    """Build the squad, process it and print the results."""
    squad = build_squad()
    grand_total = add_up_totals(squad)
    print("Athletes processed:", squad.count())
    print(f"Grand total of monthly totals: £{grand_total:,.2f}")


if __name__ == "__main__":
    main()
