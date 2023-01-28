import sys

import logging


def init_logging(level):
    return logging.basicConfig(
        level=getattr(logging, level),
        stream=sys.stdout,
    )
