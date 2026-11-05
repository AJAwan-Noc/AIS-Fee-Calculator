"""Unit tests for the input validation functions."""

import unittest

import validation


class TestValidateName(unittest.TestCase):
    """Tests for validate_name."""

    def test_valid_name(self) -> None:
        """A normal name is accepted."""
        self.assertEqual(validation.validate_name("Sam"), (True, "Sam"))

    def test_hyphen_apostrophe_and_space(self) -> None:
        """Hyphens, apostrophes and spaces are allowed."""
        result = validation.validate_name("Mary-Ann O'Neil")
        self.assertEqual(result, (True, "Mary-Ann O'Neil"))

    def test_empty_name(self) -> None:
        """An empty name is rejected with a message."""
        ok, message = validation.validate_name("")
        self.assertFalse(ok)
        self.assertIn("cannot be empty", message)

    def test_spaces_only_name(self) -> None:
        """A name made only of spaces counts as empty."""
        ok, message = validation.validate_name("   ")
        self.assertFalse(ok)

    def test_fifty_character_name_accepted(self) -> None:
        """A name of exactly 50 characters is accepted."""
        name = "A" * 50
        self.assertEqual(validation.validate_name(name), (True, name))

    def test_fifty_one_character_name_rejected(self) -> None:
        """A 51-character name is rejected and the message names 50."""
        ok, message = validation.validate_name("A" * 51)
        self.assertFalse(ok)
        self.assertIn("maximum is 50", message)

    def test_length_checked_after_stripping(self) -> None:
        """Surrounding spaces do not count towards the length."""
        name = "A" * 50
        result = validation.validate_name("  " + name + "  ")
        self.assertEqual(result, (True, name))

    def test_name_with_digits(self) -> None:
        """Digits are not allowed in a name."""
        ok, message = validation.validate_name("B0b")
        self.assertFalse(ok)
        self.assertIn("letters", message)


class TestValidatePlan(unittest.TestCase):
    """Tests for validate_plan."""

    def test_valid_plan(self) -> None:
        """A known plan is accepted."""
        self.assertEqual(
            validation.validate_plan("Beginner"), (True, "Beginner")
        )

    def test_plan_is_case_insensitive(self) -> None:
        """Any capitalisation works and the proper name is returned."""
        self.assertEqual(validation.validate_plan("eLiTe"), (True, "Elite"))

    def test_unknown_plan(self) -> None:
        """An unknown plan is rejected."""
        ok, message = validation.validate_plan("Platinum")
        self.assertFalse(ok)
        self.assertIn("not recognised", message)


class TestValidateWeight(unittest.TestCase):
    """Tests for validate_weight."""

    def test_valid_weight(self) -> None:
        """A positive number is accepted."""
        self.assertEqual(validation.validate_weight("72.5"), (True, 72.5))

    def test_text_weight(self) -> None:
        """Text such as 'abc' is rejected."""
        ok, message = validation.validate_weight("abc")
        self.assertFalse(ok)
        self.assertIn("must be a number", message)

    def test_empty_weight(self) -> None:
        """An empty weight is rejected."""
        ok, message = validation.validate_weight("")
        self.assertFalse(ok)

    def test_negative_weight(self) -> None:
        """A negative weight is rejected."""
        ok, message = validation.validate_weight("-3")
        self.assertFalse(ok)
        self.assertIn("greater than 0", message)

    def test_zero_weight(self) -> None:
        """Zero is not above 0, so it is rejected."""
        ok, message = validation.validate_weight("0")
        self.assertFalse(ok)


class TestValidateCategory(unittest.TestCase):
    """Tests for validate_category."""

    def test_81kg_light_middleweight_accepted(self) -> None:
        """81 kg is exactly the Light-Middleweight upper limit."""
        result = validation.validate_category("Light-Middleweight", 81.0)
        self.assertEqual(result, (True, "Light-Middleweight"))

    def test_81kg_middleweight_rejected(self) -> None:
        """81 kg is not over 81, so it does not fit Middleweight."""
        ok, message = validation.validate_category("Middleweight", 81.0)
        self.assertFalse(ok)
        self.assertIn("does not fit Middleweight", message)

    def test_81_5kg_light_middleweight_rejected(self) -> None:
        """81.5 kg is over the Light-Middleweight limit."""
        ok, message = validation.validate_category("Light-Middleweight", 81.5)
        self.assertFalse(ok)

    def test_100_5kg_heavyweight_accepted(self) -> None:
        """Heavyweight has no upper limit, so 100.5 kg fits."""
        result = validation.validate_category("Heavyweight", 100.5)
        self.assertEqual(result, (True, "Heavyweight"))

    def test_100kg_heavyweight_rejected(self) -> None:
        """Heavyweight is over 100 kg, so exactly 100 kg does not fit."""
        ok, message = validation.validate_category("Heavyweight", 100.0)
        self.assertFalse(ok)

    def test_category_is_case_insensitive(self) -> None:
        """Any capitalisation works and the proper name is returned."""
        result = validation.validate_category("flyweight", 50.0)
        self.assertEqual(result, (True, "Flyweight"))

    def test_unknown_category(self) -> None:
        """A category that does not exist is rejected."""
        ok, message = validation.validate_category("Featherweight", 60.0)
        self.assertFalse(ok)
        self.assertIn("not recognised", message)


class TestValidateCompetitions(unittest.TestCase):
    """Tests for validate_competitions."""

    def test_valid_competitions(self) -> None:
        """Intermediate can enter a whole number of competitions."""
        result = validation.validate_competitions("Intermediate", "2")
        self.assertEqual(result, (True, 2))

    def test_zero_competitions(self) -> None:
        """Zero is accepted for any plan, including Beginner."""
        result = validation.validate_competitions("Beginner", "0")
        self.assertEqual(result, (True, 0))

    def test_beginner_with_one_competition(self) -> None:
        """Beginner entering 1 competition is rejected with a reason."""
        ok, message = validation.validate_competitions("Beginner", "1")
        self.assertFalse(ok)
        self.assertIn("Only Intermediate and Elite", message)

    def test_five_competitions_accepted(self) -> None:
        """5 is exactly the sanity maximum and is accepted."""
        result = validation.validate_competitions("Elite", "5")
        self.assertEqual(result, (True, 5))

    def test_six_competitions_rejected(self) -> None:
        """6 is above the sanity maximum and the message names it."""
        ok, message = validation.validate_competitions("Elite", "6")
        self.assertFalse(ok)
        self.assertIn("maximum is 5", message)

    def test_huge_competitions_rejected(self) -> None:
        """The 99999 case from the edge-case script is now rejected."""
        ok, message = validation.validate_competitions("Elite", "99999")
        self.assertFalse(ok)

    def test_negative_competitions(self) -> None:
        """A negative number is rejected."""
        ok, message = validation.validate_competitions("Elite", "-3")
        self.assertFalse(ok)
        self.assertIn("whole number", message)

    def test_decimal_competitions(self) -> None:
        """A decimal is not a whole number."""
        ok, message = validation.validate_competitions("Elite", "1.5")
        self.assertFalse(ok)

    def test_text_competitions(self) -> None:
        """Text such as 'abc' is rejected."""
        ok, message = validation.validate_competitions("Elite", "abc")
        self.assertFalse(ok)

    def test_empty_competitions(self) -> None:
        """An empty answer is rejected."""
        ok, message = validation.validate_competitions("Elite", "")
        self.assertFalse(ok)


class TestValidateCoachingHours(unittest.TestCase):
    """Tests for validate_coaching_hours."""

    def test_valid_hours(self) -> None:
        """A number inside the allowed range is accepted."""
        self.assertEqual(
            validation.validate_coaching_hours("2"), (True, 2.0)
        )

    def test_zero_hours(self) -> None:
        """Zero hours is the bottom of the range and is accepted."""
        self.assertEqual(
            validation.validate_coaching_hours("0"), (True, 0.0)
        )

    def test_five_hours_accepted(self) -> None:
        """Five hours is exactly the maximum and is accepted."""
        self.assertEqual(
            validation.validate_coaching_hours("5"), (True, 5.0)
        )

    def test_five_and_a_half_hours_rejected(self) -> None:
        """5.5 hours is above the maximum."""
        ok, message = validation.validate_coaching_hours("5.5")
        self.assertFalse(ok)
        self.assertIn("between 0 and 5", message)

    def test_six_hours_rejected(self) -> None:
        """6 hours is above the maximum."""
        ok, message = validation.validate_coaching_hours("6")
        self.assertFalse(ok)

    def test_negative_hours_rejected(self) -> None:
        """Negative hours are rejected."""
        ok, message = validation.validate_coaching_hours("-3")
        self.assertFalse(ok)

    def test_text_hours_rejected(self) -> None:
        """Text such as 'abc' is rejected."""
        ok, message = validation.validate_coaching_hours("abc")
        self.assertFalse(ok)
        self.assertIn("must be a number", message)

    def test_empty_hours_rejected(self) -> None:
        """An empty answer is rejected."""
        ok, message = validation.validate_coaching_hours("")
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
