import sys
import requests
import os
from mycode import ff
#from mycode.bso_coverage import bso_coverage
from project.server.main.logger import get_logger

logger = get_logger(__name__)


def create_task_compute(args: dict) -> None:
    logger.debug(f"Creating task with args {args}")
    #error = bso_coverage.test_mother_duck()
    logger.debug(f"Task ended with error {error}")

