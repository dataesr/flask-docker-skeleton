import sys

from mycode import ff 
from application.server.main.logger import get_logger

logger = get_logger(__name__)


def create_task(args: dict) -> None:
    logger.debug(f'Creating task with args {args}')
