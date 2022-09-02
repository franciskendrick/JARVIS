import os


def get_synchronous_schedule():
    SCHEDULE_TIME = os.environ["SYNC_SCHEDULE_TIME"]
    SCHEDULE_SUBJECTS = os.environ["SYNC_SCHEDULE_SUBJECTS"]
    sync_full_schedule = {}
    for days in SCHEDULE_SUBJECTS.split(". "):
        day, subjects = days.split(" = ")
        sync_full_schedule[day] = {}
        for (time, subject) in zip(SCHEDULE_TIME.split(", "), subjects.split(", ")):
            sync_full_schedule[day][time] = subject

    return sync_full_schedule
