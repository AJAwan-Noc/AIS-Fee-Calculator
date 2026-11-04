"""Unit tests for the pricing functions."""

import unittest

import pricing


class TestTrainingCost(unittest.TestCase):
    """Tests for training_cost."""

    def test_beginner(self) -> None:
        """Beginner pays 25.00 x 4 weeks."""
        self.assertAlmostEqual(pricing.training_cost("Beginner"), 100.00)

    def test_intermediate(self) -> None:
        """Intermediate pays 30.00 x 4 weeks."""
        self.assertAlmostEqual(pricing.training_cost("Intermediate"), 120.00)

    def test_elite(self) -> None:
        """Elite pays 35.00 x 4 weeks."""
        self.assertAlmostEqual(pricing.training_cost("Elite"), 140.00)


class TestCoachingCost(unittest.TestCase):
    """Tests for coaching_cost."""

    def test_two_hours_per_week(self) -> None:
        """2 hrs/week is 2 x 9.50 x 4 = 76.00."""
        self.assertAlmostEqual(pricing.coaching_cost(2), 76.00)

    def test_zero_hours(self) -> None:
        """No coaching costs nothing."""
        self.assertAlmostEqual(pricing.coaching_cost(0), 0.00)

    def test_maximum_hours_boundary(self) -> None:
        """5 hrs/week (the maximum) is 5 x 9.50 x 4 = 190.00."""
        self.assertEqual(pricing.MAX_COACH_HOURS, 5)
        cost = pricing.coaching_cost(pricing.MAX_COACH_HOURS)
        self.assertAlmostEqual(cost, 190.00)

    def test_half_hour(self) -> None:
        """Half hours are charged proportionally: 0.5 hr is 19.00."""
        self.assertAlmostEqual(pricing.coaching_cost(0.5), 19.00)


class TestCompetitionCost(unittest.TestCase):
    """Tests for competition_cost."""

    def test_one_competition(self) -> None:
        """One competition costs 22.00."""
        self.assertAlmostEqual(pricing.competition_cost(1), 22.00)

    def test_three_competitions(self) -> None:
        """Three competitions cost 66.00."""
        self.assertAlmostEqual(pricing.competition_cost(3), 66.00)

    def test_zero_competitions(self) -> None:
        """No competitions costs nothing."""
        self.assertAlmostEqual(pricing.competition_cost(0), 0.00)


class TestMonthlyTotal(unittest.TestCase):
    """Tests for monthly_total."""

    def test_intermediate_oracle(self) -> None:
        """Intermediate, 1 competition, 2 hrs/week is 218.00."""
        total = pricing.monthly_total("Intermediate", 2, 1)
        self.assertAlmostEqual(total, 218.00)

    def test_elite_oracle(self) -> None:
        """Elite, 3 hrs/week, 0 competitions is 254.00."""
        total = pricing.monthly_total("Elite", 3, 0)
        self.assertAlmostEqual(total, 254.00)

    def test_all_zero_extras(self) -> None:
        """With no coaching or competitions, only training is charged."""
        total = pricing.monthly_total("Beginner", 0, 0)
        self.assertAlmostEqual(total, 100.00)

    def test_maximum_coaching(self) -> None:
        """Elite with 5 hrs/week is 140.00 + 190.00 = 330.00."""
        total = pricing.monthly_total("Elite", 5, 0)
        self.assertAlmostEqual(total, 330.00)


if __name__ == "__main__":
    unittest.main()
