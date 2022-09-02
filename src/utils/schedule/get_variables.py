from ..format_time import convert_timestr_to_datetime
from ..format_time import round_time
import datetime
import pytz
import json
import os

resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "..", "resources"
        )
    )

# JSON
with open(f"{resources_path}/aliases.json") as json_file:
    all_aliases = json.load(json_file)


def get_day(given_day):
    if given_day == None:  # no argument given
        with_input = False

        # Get current day
        timezone_manila = pytz.timezone("Asia/Manila")
        day = datetime.datetime.now(timezone_manila).strftime("%A")
    else:  # has an argument
        with_input = True

        # Get day
        day = None
        for key, aliases in all_aliases["day"].items():
            if given_day.lower() in aliases:
                day = key
                break

    return day, with_input


def get_learningtype(given_learningtype):
    if given_learningtype == None:
        tz_manila = pytz.timezone("Asia/Manila")
        now = datetime.datetime.now(tz_manila)
        current_time = round_time(now.strftime("%H:%M:%S"))

        # Get synchronous and asynchronous time
        SYNC_TIMES = os.environ["SYNC_SCHEDULE_TIME"]
        ASYNC_TIMES = os.environ["ASYNC_SCHEDULE_TIME"]

        # Get synchronous and asynchronous splitted times
        split_synctimes = SYNC_TIMES.split(', ')
        split_asynctimes = ASYNC_TIMES.split(', ')

        # Get synchronous and asynchronous end time
        sync_endtime = split_synctimes[-1].split(" - ")[-1]
        async_endtime = split_asynctimes[-1].split(" - ")[-1]

        # Format synchronous and asynchronous end time
        sync_endtime = round_time(sync_endtime)
        async_endtime = round_time(async_endtime)

        # Check if the current time has passed the synchronous end time
        passed_synctime = True
        synctime_difference = sync_endtime - current_time
        if not int(str(synctime_difference).count("-")):  # not passed synchronous end time
            passed_synctime = False
            synctime_difference = convert_timestr_to_datetime(
                str(synctime_difference))

        # Check if the current time has passed the asynchronous end time
        passed_asynctime = True
        asynctime_difference = async_endtime - current_time
        if not int(str(asynctime_difference).count("-")):  # not passed asynchrnous end time
            passed_asynctime = False
            asynctime_difference = convert_timestr_to_datetime(
                str(asynctime_difference))

        # Get learning type
        if not passed_synctime:  # synchronous
            learning_type = "synchronous"
        elif passed_synctime and not passed_asynctime:  # asynchronous
            learning_type = "asynchronous"
        elif passed_asynctime:  # all (classes are finished)
            learning_type = "all"

        return learning_type
    else:
        # Get learning type
        if given_learningtype == "all":
            learning_type = given_learningtype
        else:
            for key, aliases in all_aliases["learning_type"].items():
                if given_learningtype.lower() in aliases:
                    learning_type = key
                    break

    return learning_type
