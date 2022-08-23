def get_hoursleft(time_pivot):
    hour = time_pivot.hour
    if hour > 1:  # plural
        hour = f"{hour} hrs"
    elif hour == 1:  # singular
        hour = f"{hour} hr"
    else:  # none
        hour = None
    
    return hour


def get_minutesleft(time_pivot):
    min = time_pivot.minute
    if min > 1:  # plural
        min = f"{min} mins"
    elif min == 1:  # singular
        min = f"{min} min"
    else:
        min = None

    return min
