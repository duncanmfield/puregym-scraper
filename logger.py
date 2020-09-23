import config
from datetime import datetime
import logging
import sys
import time

def set_up():
    # Set up file output
    fmt = '%(asctime)s -> %(message)s'
    date_fmt = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(filename=config.log_file,
                        format=fmt,
                        datefmt=date_fmt,
                        level=logging.INFO)

    # Set up console output
    formatter = logging.Formatter('[LOG] ' + fmt, date_fmt)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

    print(f"Data will be logged at every {config.log_interval_minutes} minute interval past the hour.")
    if not config.force_log_at_start:
        print(f"First log entry will occur in {get_time_until_interval()} seconds.")
        print(f"To force a log entry at startup, set 'force_log_at_start = True' in the config.\n")
        sleep_until_interval()
    else:
        print(f"Forcing startup log entry. Next log entry will occur in {get_time_until_interval()} seconds.\n")


def get_time_until_interval():
    seconds_into_hour = datetime.now().minute * 60 + datetime.now().second
    log_interval_seconds = config.log_interval_minutes * 60
    seconds_until_interval = log_interval_seconds - (seconds_into_hour % log_interval_seconds)
    return seconds_until_interval


def sleep_until_interval():
    time.sleep(get_time_until_interval())


def log(count):
    try:
        val = int(count)
        logging.info(val)
    except ValueError:
        print(f"Value was not an integer: {count}")