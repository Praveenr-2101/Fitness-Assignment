import pytz
from pytz import timezone as pytz_timezone, UnknownTimeZoneError



def convert_to_timezone(dt, tz_name):
    """Converts a datetime object to a target timezone."""
    try:
        target_tz = pytz.timezone(tz_name)
        return dt.astimezone(target_tz)
    except UnknownTimeZoneError:
        return dt