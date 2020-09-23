import config
import logger
import re
import requests


def start():
    validate_config()
    print(f"Logging in as {config.email}.")
    session = requests.session()

    while True:
        pin = input("Please enter your pin: ")
        success = login(session, pin)
        if success:
            logger.set_up()
            break

    failures = 0
    while True:
        run_scraper(session)

        failures += 1
        if failures < 3:
            session = requests.session()
            login(session, pin)
        else:
            print("Failed to log in too many times. Skipping.")
            logger.sleep_until_interval()
            failures = 0


def validate_config():
    if len(config.log_file) == 0:
        fail_validation("[ERROR] Config 'log_file' has not been set. Aborting.")
    elif len(config.email) == 0 or config.email == "example@example.com":
        fail_validation("[ERROR] Config 'email' has not been set. Aborting.")
    elif config.log_interval_minutes < 1 or config.log_interval_minutes > 60:
        fail_validation("[ERROR] Config 'log_interval_minutes' must be between 1 and 60, inclusive. Aborting.")
    elif not type(config.force_log_at_start) is bool:
        fail_validation("[ERROR] Config 'force_log_at_start' must be True or False. Aborting.")


def fail_validation(message):
    print(message)
    exit(1)


def run_scraper(session):
    while True:
        try:
            success = scrape_page(session)
        except:
            success = False

        if success:
            logger.sleep_until_interval()
        else:
            return


def login(session, pin):
    url = "https://www.puregym.com/api/members/login/"
    payload = {"associateAccount": "false", "email": config.email, "pin": pin}
    session.headers.update({'__RequestVerificationToken': get_request_verification_token(session)})
    response = session.post(url, payload)

    success = response.status_code == 200 and next(response.iter_lines(), None) is None
    if success:
        print(f"Successfully logged in as {config.email}.\n")
    else:
        print(f"Failed to log in as {config.email}.")

    return success


def get_request_verification_token(session):
    for raw_line in session.get("https://www.puregym.com/login/").iter_lines():
        line = str(raw_line)
        if "__RequestVerificationToken" in line:
            return line.split("value=")[1].split("\"")[1]

    return ""


def scrape_page(session):
    url = "https://www.puregym.com/members/"
    response = session.get(url)

    for raw_line in response.iter_lines():
        line = str(raw_line)

        if is_correct_line(line):
            logger.log(get_count(line))
            return True

    return False


def is_correct_line(line):
    return re.search("Hello [\\S]+, there are", line)


def get_count(line):
    text = line.split(">")[1].split("<")[0]  # text = "x of y people"
    count = text.split(" ")[0]  # count = "x"
    count = count.replace("+", "")  # Deals with '100+' scenario
    return count


start()