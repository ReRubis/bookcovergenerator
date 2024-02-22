import logging


def setup_logging(name: str) -> None:
    base_logger = logging.getLogger(name)
    base_logger.setLevel(logging.INFO)


# Setup logging
setup_logging(__package__)


del setup_logging
