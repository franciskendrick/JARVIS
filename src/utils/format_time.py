import datetime


def formattime_to_twelevehour(time):
    # Convert time into a datetime object
    time = datetime.datetime.strptime(time, "%H:%M:%S")

    # Get tweleve hour time format
    time = time.time()
    twelvehour_format = time.strftime("%I:%M")

    # Get meridian
    meridian = "PM" if time.hour >= 12 else "AM"

    # Return
    return f"{twelvehour_format} {meridian}"


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
