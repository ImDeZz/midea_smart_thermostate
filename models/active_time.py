from datetime import datetime
from typing import List, Optional


class ActiveTime:
    """
    Represents a single active time with start and end times, day, and temperature range.
    """
    def __init__(self, start_time: str, end_time: str, day: str, min_temp: float, max_temp: float):
        self.start_time = start_time
        self.end_time = end_time
        self.day = day.upper()  # Ensure day values are uppercase for consistency
        self.min_temp = min_temp
        self.max_temp = max_temp

    def get_is_between_active_times(self) -> bool:
        """
        Check if the current time is between the active time range for this ActiveTime.
        """
        start = datetime.strptime(self.start_time, "%H:%M").time()
        end = datetime.strptime(self.end_time, "%H:%M").time()
        now = datetime.now().time()

        if start <= end:
            return start <= now <= end
        else:
            return now >= start or now <= end

    def is_day_matching(self) -> bool:
        """
        Check if the current day matches the day condition for this ActiveTime.
        """
        now = datetime.now()
        now_day = now.strftime("%A").upper()
        
        if self.day == "ALL":
            return True
        if self.day == "WEEKDAYS" and now_day in {"MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"}:
            return True
        if self.day == "WEEKENDS" and now_day in {"SATURDAY", "SUNDAY"}:
            return True
        return self.day == now_day[:3]

    def __repr__(self):
        return (
            f"ActiveTime(start_time={self.start_time!r}, end_time={self.end_time!r}, "
            f"day={self.day!r}, min_temp={self.min_temp!r}, max_temp={self.max_temp!r})"
        )


class ActiveTimeList:
    """
    Represents a list of active times and provides methods to check overall activity.
    """
    def __init__(self, active_times: Optional[List[ActiveTime]] = None):
        self.active_times = active_times if active_times else []

    def add_active_time(self, active_time: ActiveTime):
        """Add an active time to the list."""
        self.active_times.append(active_time)

    def get_active(self) -> (ActiveTime | None):
        """
        Check if at least one active time in the list is currently active.
        """
        for active_time in self.active_times:
            if active_time.is_day_matching() and active_time.get_is_between_active_times():
                return active_time
        return None

    def __repr__(self):
        return f"ActiveTimeList(active_times={self.active_times!r})"
