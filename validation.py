"""Input validation for the fee calculator.

Every validate_* function returns a tuple (ok, value_or_message).
If ok is True the second item is the cleaned value. If ok is False the
second item is a friendly message to show before asking again.
"""

import math

from pricing import (
    MAX_COACH_HOURS,
    MAX_COMPETITIONS,
    WEEKLY_FEES,
    WEIGHT_CATEGORIES,
)

NAME_EXTRA_CHARACTERS = " -'"
# Sanity limit, not a client rule: keeps the GUI layout readable.
MAX_NAME_LENGTH = 50


def parse_number(text: str) -> tuple:
    """Turn text into a finite number, returning (ok, number)."""
    try:
        number = float(text.strip())
    except ValueError:
        return (False, 0.0)
    # float() accepts "nan" and "inf", which are not real measurements.
    if not math.isfinite(number):
        return (False, 0.0)
    return (True, number)


def validate_name(text: str) -> tuple:
    """Check the name is not empty and uses only allowed characters."""
    name = text.strip()
    if name == "":
        return (False, "The name cannot be empty. Please enter a name.")
    if len(name) > MAX_NAME_LENGTH:
        return (
            False,
            "That name is too long. The maximum is "
            + str(MAX_NAME_LENGTH)
            + " characters.",
        )
    for character in name:
        if not character.isalpha() and character not in NAME_EXTRA_CHARACTERS:
            return (
                False,
                "The name can only contain letters, spaces, hyphens and "
                "apostrophes. Please try again.",
            )
    return (True, name)


def validate_plan(text: str) -> tuple:
    """Check the plan is one of the plans in WEEKLY_FEES (any case)."""
    wanted = text.strip().lower()
    for plan in WEEKLY_FEES:
        if plan.lower() == wanted:
            return (True, plan)
    plan_names = ", ".join(WEEKLY_FEES)
    return (False, "Plan not recognised. Please choose one of: " + plan_names)


def validate_weight(text: str) -> tuple:
    """Check the weight is a number above 0 (in kg)."""
    ok, weight = parse_number(text)
    if not ok:
        return (False, "The weight must be a number, for example 72.5.")
    if weight <= 0:
        return (False, "The weight must be greater than 0 kg.")
    return (True, weight)


def find_band(category: str) -> tuple:
    """Return (lower, upper) kg limits for a category, or None if unknown.

    The lower limit is the upper limit of the category before it. The
    upper limit is None for Heavyweight. A weight fits when it is above
    the lower limit and no more than the upper limit.
    """
    lower = 0
    for name, upper in WEIGHT_CATEGORIES:
        if name == category:
            return (lower, upper)
        lower = upper
    return None


def describe_band(lower: float, upper) -> str:
    """Describe a weight band in words for use in messages."""
    if upper is None:
        return "over " + str(lower) + " kg"
    if lower == 0:
        return "up to " + str(upper) + " kg"
    return "over " + str(lower) + " kg and up to " + str(upper) + " kg"


def validate_category(text: str, weight: float) -> tuple:
    """Check the category exists and the weight fits its band."""
    wanted = text.strip().lower()
    names = []
    for name, upper in WEIGHT_CATEGORIES:
        if name.lower() == wanted:
            return check_weight_fits(name, weight)
        names.append(name)
    names = ", ".join(names)
    return (False, "Category not recognised. Please choose one of: " + names)


def check_weight_fits(category: str, weight: float) -> tuple:
    """Check a weight sits inside the band of a known category."""
    lower, upper = find_band(category)
    too_light = weight <= lower
    too_heavy = upper is not None and weight > upper
    if too_light or too_heavy:
        return (
            False,
            str(weight)
            + " kg does not fit "
            + category
            + " ("
            + describe_band(lower, upper)
            + "). Please choose the category that matches the weight.",
        )
    return (True, category)


def validate_competitions(plan: str, text: str) -> tuple:
    """Check competitions is a whole number 0 or more, and 0 for Beginner."""
    entered = text.strip()
    if not entered.isdecimal():
        return (False, "Please enter a whole number of 0 or more.")
    competitions = int(entered)
    if plan == "Beginner" and competitions > 0:
        return (
            False,
            "Beginners cannot enter competitions. Only Intermediate and "
            "Elite members can compete, so please enter 0.",
        )
    if competitions > MAX_COMPETITIONS:
        return (
            False,
            "That is too many competitions. The maximum is "
            + str(MAX_COMPETITIONS)
            + " per month.",
        )
    return (True, competitions)


def validate_coaching_hours(text: str) -> tuple:
    """Check coaching hours per week is between 0 and MAX_COACH_HOURS."""
    ok, hours = parse_number(text)
    if not ok:
        return (False, "Coaching hours must be a number, for example 2.5.")
    if hours < 0 or hours > MAX_COACH_HOURS:
        return (
            False,
            "Coaching hours per week must be between 0 and "
            + str(MAX_COACH_HOURS)
            + ".",
        )
    return (True, hours)
