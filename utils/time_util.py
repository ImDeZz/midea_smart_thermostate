from datetime import datetime

def get_is_between_active_times(start_time: str, end_time: str) -> bool:
    """
    Check if the current time is between the start and end times.

    Args:
        start_time (str): Start time in "HH:MM" format (24-hour clock).
        end_time (str): End time in "HH:MM" format (24-hour clock).

    Returns:
        bool: True if the current time is between the start and end times, False otherwise.
    """
    # Parse the start and end times
    start = datetime.strptime(start_time, "%H:%M").time()
    end = datetime.strptime(end_time, "%H:%M").time()
    
    # Get the current time
    now = datetime.now().time()

    # Handle cases where the time range crosses midnight
    if start <= end:
        return start <= now <= end
    else:
        return now >= start or now <= end
