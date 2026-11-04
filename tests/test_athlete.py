"""Unit tests for the Athlete and Squad classes."""

import unittest

from athlete import Athlete, Squad


def make_intermediate() -> Athlete:
    """Build the Intermediate oracle athlete (total 218.00)."""
    return Athlete("Sam", "Intermediate", 80.0, "Light-Middleweight", 1, 2)


def make_elite() -> Athlete:
    """Build the Elite oracle athlete (total 254.00)."""
    return Athlete("Alex", "Elite", 95.0, "Light-Heavyweight", 0, 3)


class TestAthlete(unittest.TestCase):
    """Tests for the Athlete class."""

    def test_details_are_stored(self) -> None:
        """The constructor keeps every detail it is given."""
        athlete = make_intermediate()
        self.assertEqual(athlete.name, "Sam")
        self.assertEqual(athlete.plan, "Intermediate")
        self.assertEqual(athlete.weight, 80.0)
        self.assertEqual(athlete.category, "Light-Middleweight")
        self.assertEqual(athlete.competitions, 1)
        self.assertEqual(athlete.coach_hours, 2)

    def test_intermediate_total(self) -> None:
        """Intermediate, 1 competition, 2 hrs/week totals 218.00."""
        lines, total = make_intermediate().monthly_breakdown()
        self.assertAlmostEqual(total, 218.00)

    def test_elite_total(self) -> None:
        """Elite, 3 hrs/week, 0 competitions totals 254.00."""
        lines, total = make_elite().monthly_breakdown()
        self.assertAlmostEqual(total, 254.00)

    def test_breakdown_labels(self) -> None:
        """There is one line each for training, coaching, competitions."""
        lines, total = make_intermediate().monthly_breakdown()
        labels = []
        for label, working, cost in lines:
            labels.append(label)
        self.assertEqual(labels, ["Training", "Coaching", "Competitions"])

    def test_breakdown_costs(self) -> None:
        """Line costs for the Intermediate oracle are 120, 76 and 22."""
        lines, total = make_intermediate().monthly_breakdown()
        self.assertAlmostEqual(lines[0][2], 120.00)
        self.assertAlmostEqual(lines[1][2], 76.00)
        self.assertAlmostEqual(lines[2][2], 22.00)

    def test_line_costs_add_up_to_total(self) -> None:
        """The three line costs add up to the total."""
        lines, total = make_elite().monthly_breakdown()
        line_sum = 0
        for label, working, cost in lines:
            line_sum = line_sum + cost
        self.assertAlmostEqual(line_sum, total)

    def test_breakdown_working_text(self) -> None:
        """The working column shows how each cost was calculated."""
        lines, total = make_intermediate().monthly_breakdown()
        self.assertEqual(lines[0][1], "£30.00 x 4 weeks")
        self.assertEqual(lines[1][1], "2 hrs/week x £9.50 x 4 weeks")
        self.assertEqual(lines[2][1], "1 x £22.00")

    def test_zero_coaching_and_competitions(self) -> None:
        """A Beginner with no extras only pays for training."""
        athlete = Athlete("Jo", "Beginner", 60.0, "Flyweight", 0, 0)
        lines, total = athlete.monthly_breakdown()
        self.assertAlmostEqual(total, 100.00)
        self.assertAlmostEqual(lines[1][2], 0.00)
        self.assertAlmostEqual(lines[2][2], 0.00)


class TestSquad(unittest.TestCase):
    """Tests for the Squad class."""

    def test_new_squad_is_empty(self) -> None:
        """A new squad has no athletes."""
        squad = Squad()
        self.assertEqual(squad.count(), 0)
        self.assertEqual(squad.get_all(), [])

    def test_add_athlete(self) -> None:
        """Adding an athlete increases the count and stores them."""
        squad = Squad()
        athlete = make_intermediate()
        squad.add_athlete(athlete)
        self.assertEqual(squad.count(), 1)
        self.assertIs(squad.get_all()[0], athlete)

    def test_add_several_athletes_in_order(self) -> None:
        """Athletes are kept in the order they were added."""
        squad = Squad()
        first = make_intermediate()
        second = make_elite()
        squad.add_athlete(first)
        squad.add_athlete(second)
        self.assertEqual(squad.count(), 2)
        self.assertEqual(squad.get_all(), [first, second])


if __name__ == "__main__":
    unittest.main()
