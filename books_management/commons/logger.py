import logging


class Logger:
    def __init__(self) -> None:
        logging.basicConfig(format="[%(levelname)s: %(asctime)s] %(name)s | %(message)s", level=logging.INFO)
        self._logging_instance = logging.getLogger(__name__)

    def info(self, message: str) -> None:
        """Logs an info message."""
        self._logging_instance.info(message)

    def error(self, message: str) -> None:
        """Logs an error message."""
        self._logging_instance.error(message)

    def warning(self, message: str) -> None:
        """Logs a warning message."""
        self._logging_instance.warning(message)

    def debug(self, message: str) -> None:
        """Logs a debug message."""
        self._logging_instance.debug(message)
