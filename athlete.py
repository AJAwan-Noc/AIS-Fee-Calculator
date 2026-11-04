"""Athlete and Squad classes for the fee calculator."""

from pricing import (
    COACH_RATE,
    COMP_FEE,
    WEEKLY_FEES,
    WEEKS,
    coaching_cost,
    competition_cost,
    monthly_total,
    training_cost,
)


class Athlete:
    """One member of the club and the details needed to work out fees."""

    def __init__(
        self,
        name: str,
        plan: str,
        weight: float,
        category: str,
        competitions: int,
        coach_hours: float,
    ) -> None:
        """Store the athlete's details (already validated)."""
        self.name = name
        self.plan = plan
        self.weight = weight
        self.category = category
        self.competitions = competitions
        self.coach_hours = coach_hours

    def monthly_breakdown(self) -> tuple:
        """Return (lines, total). Each line is (label, working, cost)."""
        weekly_fee = WEEKLY_FEES[self.plan]
        training_working = f"£{weekly_fee:.2f} x {WEEKS} weeks"
        coaching_working = (
            f"{self.coach_hours:g} hrs/week x £{COACH_RATE:.2f} "
            f"x {WEEKS} weeks"
        )
        competition_working = (
            f"{self.competitions} x £{COMP_FEE:.2f}"
        )
        lines = [
            ("Training", training_working, training_cost(self.plan)),
            (
                "Coaching",
                coaching_working,
                coaching_cost(self.coach_hours),
            ),
            (
                "Competitions",
                competition_working,
                competition_cost(self.competitions),
            ),
        ]
        total = monthly_total(self.plan, self.coach_hours, self.competitions)
        return (lines, total)


class Squad:
    """A group of athletes registered with the club."""

    def __init__(self) -> None:
        """Start with no athletes."""
        self.athletes = []

    def add_athlete(self, athlete: Athlete) -> None:
        """Register an athlete in the squad."""
        self.athletes.append(athlete)

    def get_all(self) -> list:
        """Return the list of all registered athletes."""
        return self.athletes

    def count(self) -> int:
        """Return how many athletes are registered."""
        return len(self.athletes)
