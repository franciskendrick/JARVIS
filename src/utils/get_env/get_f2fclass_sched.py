import os

TIME = os.environ["F2FCLASS_SCHEDULE_TIME"]


def get_subjects(section):
    subjects = {
        "Einstien": os.environ["EINSTIEN_CLASS_SCHEDULE_SUBJECTS"],
        "Newton": os.environ["NEWTON_CLASS_SCHEDULE_SUBJECTS"],
        "Maxwell": os.environ["MAXWELL_CLASS_SCHEDULE_SUBJECTS"]
    }

    return subjects[section]


def get_f2fclass_schedule(section, day):
    SUBJECTS = get_subjects(section)
    f2f_schedule = {}
    for time, subjects in zip(TIME.split(", "), SUBJECTS.split(", ")):
        subjects = subjects.split("; ")
        if len(subjects) > 1:
            subject = subjects[0] if day == "Tuesday" else subjects[1]
        else:
            [subject] = subjects 

        f2f_schedule[time] = subject

    return f2f_schedule
