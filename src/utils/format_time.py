import datetime


def formattime_to_twelvehour(time):
    # Get hours and minutes
    hours, minutes, _ = time.split(":")
    hours, minutes = int(hours), int(minutes)

    # Get meridian
    meridian = "AM"
    if hours > 12:
        meridian = "PM"
        hours -= 12

    # Return
    return ("%02d:%02d " + meridian) % (hours, minutes)


def convert_timestr_to_datetime(time):
    time = [int(t) for t in time.split(":")]
    return datetime.time(*time)


def round_time(time):
    # Get date
    date = datetime.date.today()

    # Get time
    time = f"{time[:-3]}:00"
    time = convert_timestr_to_datetime(time)

    # Return
    return datetime.datetime.combine(date, time)
