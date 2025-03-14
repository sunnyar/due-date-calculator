import unittest
import datetime
from due_date_calculator import DueDateCalculator


class TestDueDateCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = DueDateCalculator()

    def test_same_day_calculation(self):
        """Test calculation when due date is on the same day."""
        # Submit at 9 AM, due 4 hours later (1 PM same day)
        submit_date = datetime.datetime(2025, 3, 10, 9, 0)  # Monday 9 AM
        due_date = self.calculator.calculate_due_date(submit_date, 4)
        expected = datetime.datetime(2025, 3, 10, 13, 0)  # Monday 1 PM
        self.assertEqual(due_date, expected)

    def test_next_day_calculation(self):
        """Test calculation when due date is on the next working day."""
        # Submit at 2 PM, due 6 hours later (spans to next day)
        submit_date = datetime.datetime(2025, 3, 10, 14, 0)  # Monday 2 PM
        due_date = self.calculator.calculate_due_date(submit_date, 6)
        expected = datetime.datetime(2025, 3, 11, 12, 0)  # Tuesday 12 PM
        self.assertEqual(due_date, expected)

    def test_multi_day_calculation(self):
        """Test calculation when due date spans multiple working days."""
        # Submit at 2:12 PM Tuesday, due 16 hours later (spans to Thursday)
        submit_date = datetime.datetime(2025, 3, 11, 14, 12)  # Tuesday 2:12 PM
        due_date = self.calculator.calculate_due_date(submit_date, 16)
        expected = datetime.datetime(2025, 3, 13, 14, 12)  # Thursday 2:12 PM
        self.assertEqual(due_date, expected)

    def test_weekend_spanning_calculation(self):
        """Test calculation when timeframe spans a weekend."""
        # Submit Friday 2 PM, due 9 hours later (spans to Monday)
        submit_date = datetime.datetime(2025, 3, 14, 14, 0)  # Friday 2 PM
        due_date = self.calculator.calculate_due_date(submit_date, 9)
        expected = datetime.datetime(2025, 3, 17, 15, 0)  # Monday 3 PM
        self.assertEqual(due_date, expected)

    def test_exactly_end_of_day(self):
        """Test calculation when submit time is at end of working day."""
        # Submit at 4:59 PM, due 8 hours later (next day)
        submit_date = datetime.datetime(2025, 3, 10, 16, 59)  # Monday 4:59 PM
        due_date = self.calculator.calculate_due_date(submit_date, 8)
        expected = datetime.datetime(2025, 3, 11, 16, 59)  # Tuesday 4:59 PM
        self.assertEqual(due_date, expected)

    def test_zero_turnaround_time(self):
        """Test with zero turnaround time."""
        submit_date = datetime.datetime(2025, 3, 10, 14, 0)  # Monday 2 PM
        due_date = self.calculator.calculate_due_date(submit_date, 0)
        self.assertEqual(due_date, submit_date)

    def test_non_working_hours_input(self):
        """Test with submit date outside working hours."""
        # Submit at 8 AM (before working hours)
        submit_date = datetime.datetime(2025, 3, 10, 8, 0)  # Monday 8 AM
        with self.assertRaises(ValueError) as cm:
            self.calculator.calculate_due_date(submit_date, 8)
        self.assertEqual(
            str(cm.exception),
            "Submit date must be during working hours (9AM to 5PM, Monday to Friday)",
        )

        # Submit at 5:01 PM (after working hours)
        submit_date = datetime.datetime(2025, 3, 10, 17, 1)  # Monday 5:01 PM
        with self.assertRaises(ValueError) as cm:
            self.calculator.calculate_due_date(submit_date, 8)
        self.assertEqual(
            str(cm.exception),
            "Submit date must be during working hours (9AM to 5PM, Monday to Friday)",
        )

    def test_non_working_day_input(self):
        """Test with submit date on a non-working day."""
        # Submit on Saturday
        submit_date = datetime.datetime(2025, 3, 15, 10, 0)  # Saturday 10 AM
        with self.assertRaises(ValueError) as cm:
            self.calculator.calculate_due_date(submit_date, 8)
        self.assertEqual(
            str(cm.exception),
            "Submit date must be during working hours (9AM to 5PM, Monday to Friday)",
        )

    def test_negative_turnaround_time(self):
        """Test with negative turnaround time."""
        submit_date = datetime.datetime(2025, 3, 10, 14, 0)  # Monday 2 PM
        with self.assertRaises(ValueError) as cm:
            self.calculator.calculate_due_date(submit_date, -5)
        self.assertEqual(str(cm.exception), "Turnaround time cannot be negative")

    def test_long_turnaround_time(self):
        """Test with a turnaround time spanning multiple weeks."""
        # Submit Monday 10 AM, due 80 hours later (spans 2 weeks)
        submit_date = datetime.datetime(2025, 3, 10, 10, 0)  # Monday 10 AM
        due_date = self.calculator.calculate_due_date(submit_date, 80)
        expected = datetime.datetime(2025, 3, 24, 10, 0)  # Monday after 2 weeks, 10 AM
        self.assertEqual(due_date, expected)


if __name__ == "__main__":
    unittest.main()
