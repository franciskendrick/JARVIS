from ..format_time import convert_timestr_to_datetime 
from .get_timeleft import get_hoursleft, get_minutesleft


def get_classstarted_title(current_time, start_time):
    # Get how much time has elapsed
    time_elapsed = convert_timestr_to_datetime(
        str(current_time - start_time))

    # Get how much time left
    hour = get_hoursleft(time_elapsed)
    min = get_minutesleft(time_elapsed)

    # Time Left String
    if hour != None and min != None:  # with both hour and minutes
        message = f"Class started {hour} and {min} ago!"
    elif hour != None and min == None:  # with hour, but no minutes
        message = f"Class started {hour} ago!"
    elif hour == None and min != None:  # no hour, but with minutes
        message = f"Class started {min} ago!"

    # Return
    return message


def get_classnotstarted_title(starttime_difference):
    # Get how much time left
    hour = get_hoursleft(starttime_difference)
    min = get_minutesleft(starttime_difference)

    # Time left string
    if hour != None and min != None:  # with both hour and minutes
        message = f"__{hour} and {min} left__ utill class starts!"
    elif hour != None and min == None:  # with hour, but no minutes
        message = f"__{hour} left__ utill class starts!"
    elif hour == None and min != None:  # no hour, but with minutes
        message = f"__{min} left__ utill class starts!"

    # Return
    return message
