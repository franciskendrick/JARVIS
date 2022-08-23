import datetime


def format_time(time):
    # Convert time into a datetime object
    time = datetime.datetime.strptime(time, "%H:%M:%S")

    # Get tweleve hour time format
    time = time.time()
    twelvehour_format = time.strftime("%I:%M")

    # Get meridian
    meridian = "PM" if time.hour >= 12 else "AM"

    # Return
    return f"{twelvehour_format} {meridian}"
