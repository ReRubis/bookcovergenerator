import logging

from rich.logging import RichHandler


def setup_logging(name: str) -> None:
    base_logger = logging.getLogger()
    base_logger.addHandler(RichHandler(
        rich_tracebacks=True,
        keywords=[],
    ))
    base_logger.setLevel(logging.INFO)
