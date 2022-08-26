import os


def get_synchronous_schedule():
    SCHEDULE_TIME = os.environ["SCHEDULE_TIME"]
    SCHEDULE_SUBJECTS = os.environ["SCHEDULE_SUBJECTS"]
    full_schedule = {}
    for days in SCHEDULE_SUBJECTS.split(". "):
        day, subjects = days.split(" = ")
        full_schedule[day] = {}
        for (time, subject) in zip(SCHEDULE_TIME.split(", "), subjects.split(", ")):
            full_schedule[day][time] = subject

    return full_schedule
