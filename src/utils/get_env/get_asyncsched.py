import os


def get_asynchronous_schedule():
    SCHEDULE_TIME = os.environ["ASYNC_SCHEDULE_TIME"]
    SCHEDULE_SUBJECTS = os.environ["ASYNC_SCHEDULE_SUBJECTS"]
    async_full_schedule = {}
    for days in SCHEDULE_SUBJECTS.split(". "):
        day, subjects = days.split(" = ")
        async_full_schedule[day] = {}
        for (time, subject) in zip(SCHEDULE_TIME.split(", "), subjects.split(", ")):
            async_full_schedule[day][time] = subject

    return async_full_schedule
