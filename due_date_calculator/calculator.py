from datetime import datetime, timedelta
import logging


class DueDateCalculator:
    """
    A class that calculates due dates for issues in an issue tracking system.

    The calculator takes into account working hours (9AM to 5PM)
    and working days (Monday to Friday).
    """

    # Working hours and days
    WORK_START_HOUR = 9
    WORK_END_HOUR = 17
    WORK_HOURS_PER_DAY = WORK_END_HOUR - WORK_START_HOUR
    # Monday (0) to Friday (4)
    WORKING_DAYS = range(0, 5)

    def calculate_due_date(
        self, submit_date: datetime, turnaround_hours: int
    ) -> datetime:
        """
        Calculate the due date for an issue based on the submit date and turnaround time.

        Args:
            submit_date (datetime): The date and time when the issue was submitted.
            turnaround_hours (int): The turnaround time in working hours.

        Returns:
            datetime: The date and time when the issue is due to be resolved.

        Raises:
            ValueError: If the submit_date is not during working hours or
                    if turnaround_hours is negative.
        """

        # Validate inputs
        if not self._is_during_working_hours(submit_date):
            raise ValueError(
                "Submit date must be during working hours (9AM to 5PM, Monday to Friday)"
            )

        if turnaround_hours < 0:
            raise ValueError("Turnaround time cannot be negative")

        if turnaround_hours == 0:
            return submit_date

        # Calculate due date
        current_date = submit_date
        remaining_hours = turnaround_hours

        # Handle remaining hours on the first day
        hours_left_today = self._get_remaining_work_hours_in_day(current_date)

        if remaining_hours <= hours_left_today:
            # If we can complete within today's remaining work hours
            return current_date + timedelta(hours=remaining_hours)

        # Use up today's remaining hours
        remaining_hours -= hours_left_today

        # Move to start of next working day
        current_date = self._get_next_working_day(current_date)

        # Handle full working days
        while remaining_hours >= self.WORK_HOURS_PER_DAY:
            remaining_hours -= self.WORK_HOURS_PER_DAY
            current_date = self._get_next_working_day(current_date)

        # Handle remaining hours on the last day
        if remaining_hours > 0:
            # Start from work start hour
            current_date = datetime(
                current_date.year,
                current_date.month,
                current_date.day,
                self.WORK_START_HOUR,
                0,
                0,
            )
            current_date += timedelta(hours=remaining_hours)

        return current_date

    def _is_during_working_hours(self, date_time: datetime) -> bool:
        """
        Check if the given date and time is during working hours.

        Working hours are defined as 9AM to 5PM, Monday to Friday.

        Args:
            date_time (datetime): The date and time to check.

        Returns:
            datetime: The start of the next working day at 9 AM.
        """

        is_working_day = date_time.weekday() in self.WORKING_DAYS
        is_working_hour = (
            self.WORK_START_HOUR <= date_time.hour < self.WORK_END_HOUR
        ) or (date_time.hour == self.WORK_END_HOUR and date_time.minute == 0)

        return is_working_day and is_working_hour

    def _get_remaining_work_hours_in_day(self, date_time: datetime) -> float:
        """
        Get the remaining work hours in the given day.

        Args:
            date_time (datetime): The date and time to check.

        Returns:
            float: The remaining work hours in the day.
        """

        return (
            self.WORK_END_HOUR
            - date_time.hour
            - (date_time.minute / 60)
            - (date_time.second / 3600)
        )

    def _get_next_working_day(self, date_time: datetime) -> datetime:
        """
        Get the start of the next working day from the given date.

        Args:
            date_time (datetime): The date and time to start from.

        Returns:
            datetime: The start of the next working day at 9 AM.
        """

        # Start with the next calendar day
        next_day = date_time + timedelta(days=1)

        # Reset to 9 AM
        next_day = datetime(
            next_day.year, next_day.month, next_day.day, self.WORK_START_HOUR, 0, 0
        )

        # If it's a weekend, move to next week (Monday)
        while next_day.weekday() not in self.WORKING_DAYS:
            next_day += timedelta(days=1)

        return next_day


# Example usage
def main():

    # Configure logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    calculator = DueDateCalculator()
    # Example from requirements: reported at 2:12PM on Friday with 16 hours turnaround
    submit_date = datetime(2025, 3, 14, 14, 12)
    turnaround_hours = 16

    try:
        due_date = calculator.calculate_due_date(submit_date, turnaround_hours)
        date_format = "%Y-%m-%d %H:%M"
        logging.info(
            f"Submit Date: {submit_date.strftime(date_format)} (Friday 2:12 PM)"
        )
        logging.info(f"Turnaround: {turnaround_hours} working hours")
        logging.info(f"Due Date: {due_date.strftime(date_format)} (Tuesday 2:12 PM)")

    except ValueError as e:
        logging.error(f"Error: {e}")


# Run the example usage if this script is executed directly
if __name__ == "__main__":
    main()
