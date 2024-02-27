import os
import psutil
from enum import Enum
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException


def get_local_driver():
    options = Options()
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(chrome_options=options,
                              # service_args=[
                              #     '--verbose',
                              #     '--log-path=/opt/django-apps/it4each/scraping/selenium.log'
                              # ]
                              )

    return driver


def get_remote_driver():
    options = Options()
    options.add_argument('--verbose')

    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub',
        desired_capabilities={**DesiredCapabilities.CHROME, **options.to_capabilities()})

    return driver


def get_driver():
    try:
        return get_local_driver()
    except WebDriverException:
        return get_remote_driver()


def log_memory_usage():
    mem = psutil.virtual_memory()
    print("Memory usage: {} total; {} available ({}%)".format(mem.total, mem.available, (100 - mem.percent)))


def _get_pid_file_path(name):
    return os.path.join('/tmp', name + '.pid')


def update_pid_file(name):
    """
    Creates or updates a temporary file, containing the PID of the current process.
    """
    path = _get_pid_file_path(name)
    pid = os.getpid()
    with open(path, 'w') as f:
        f.write(str(pid))


def read_pid_file(name) -> Optional[int]:
    """
    Reads the PID from the PID file or returns None if the file doesn't exist.
    """
    path = _get_pid_file_path(name)
    try:
        with open(path) as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return None


def delete_pid_file(name):
    """
    Deletes the PID file if it exists.
    Run this if the process ended successfully.
    """
    path = _get_pid_file_path(name)
    if os.path.exists(path):
        os.remove(path)


class RunStatus(Enum):
    # The process has finished OK last time: PID file is absent
    FINISHED_OK = 1
    # The process has finished with an error: PID file is present and the PID
    # is not taken by any running process.
    ERRORED = 2
    # The process is still running.
    STILL_RUNNING = 3


def get_last_run_status(name) -> RunStatus:
    """
    Checked the status of the last run of the script using the PID file.
    """
    pid = read_pid_file(name)
    if pid is None:
        return RunStatus.FINISHED_OK

    for proc in psutil.process_iter():
        if proc.pid == pid:
            return RunStatus.STILL_RUNNING

    return RunStatus.ERRORED
