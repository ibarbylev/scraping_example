#!/usr/bin/env python
import importlib
import os
import traceback
import logging
import sys
from datetime import datetime

from croniter import croniter

from settings import SCHEDULE, OUT_DIR

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='[%(asctime)s %(levelname)s %(name)s] %(message)s')
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)

    for task in SCHEDULE:
        try:
            script_name = task['script']
            module = importlib.import_module('scripts.' + script_name)

            if not croniter.match(task['when'], datetime.now()):
                it = croniter(task['when'], datetime.now())
                next_run = it.get_next(datetime)
                logger.info("{} is skipped. It will run at {}".format(script_name, next_run))
                continue

            logger.info("Running %s", script_name)
            module.run(**task)

        except Exception:
            logger.error("Task failed: %s", traceback.format_exc())
