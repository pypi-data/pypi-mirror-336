import os
import sys
import logging
from colorama import init, Fore
from logging.handlers import RotatingFileHandler


class ColoredFormatter(logging.Formatter):
    """
    A custom logging formatter that adds color to log messages based on their severity level.
    """

    COLORS = {
        "DEBUG": Fore.BLUE,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA,
    }

    def format(self, record):
        """
        Format the log message with color based on the log level.
        """
        log_message = super().format(record)
        log_level = record.levelname

        if log_level in self.COLORS:
            return f"{self.COLORS[log_level]}{log_message}{Fore.RESET}"
        else:
            return log_message


class EasyLog:
    """
    A utility class for setting up a logging system with both file and console handlers.
    It supports rotating file handlers and colored console output.
    """

    _logger = None

    def __init__(
        self,
        log_folder="/tmp/out/easylog",
        log_file="log.log",
        log_level=logging.INFO,
        log_backup=2,
        max_bytes=80 * 1024 * 1024,
    ):
        """
        Initialize the EasyLog with custom parameters.

        :param log_folder: The directory where log files will be stored.
        :param log_file: The name of the log file.
        :param log_level: The logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).
        :param log_backup: The number of backup log files to keep.
        :param max_bytes: The maximum size of each log file in bytes.
        """
        self.log_folder = log_folder
        self.log_file = log_file
        self.log_level = log_level
        self.log_backup = log_backup
        self.max_bytes = max_bytes

    def get_logger(self):
        """
        Get the configured logger instance. If the logger is not already initialized,
        it will be set up with the specified parameters.

        :return: A configured logging.Logger instance.
        """
        if EasyLog._logger is None:
            # Clear existing log files in the log folder
            if os.path.exists(self.log_folder):
                for log_file in os.listdir(self.log_folder):
                    log_file_path = os.path.join(self.log_folder, log_file)
                    if os.path.isfile(log_file_path):
                        os.remove(log_file_path)

            # Create the log folder if it does not exist
            if not os.path.exists(self.log_folder):
                os.makedirs(self.log_folder)

            EasyLog._logger = logging.getLogger(__name__)
            EasyLog._logger.setLevel(self.log_level)

            # Set up the file handler for logging to a file
            log_file_path = os.path.join(self.log_folder, self.log_file)
            file_handler = RotatingFileHandler(
                log_file_path,
                maxBytes=self.max_bytes,
                backupCount=self.log_backup,
                encoding="utf-8",
            )
            file_formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d - %(funcName)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(file_formatter)
            EasyLog._logger.addHandler(file_handler)

            # Initialize colorama for colored console output
            init(autoreset=True)

            # Set up the console handler for logging to the terminal
            console_handler = logging.StreamHandler()
            console_formatter = ColoredFormatter(
                "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d - %(funcName)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            console_handler.setFormatter(console_formatter)
            EasyLog._logger.addHandler(console_handler)

            # Set up an exception hook to log uncaught exceptions
            def log_exception(exc_type, exc_value, exc_traceback):
                EasyLog._logger.error(
                    "Uncaught exception",
                    exc_info=(exc_type, exc_value, exc_traceback),
                )

            sys.excepthook = log_exception

        return EasyLog._logger

    def show_logger_config(self):
        """
        Display the current logger configuration.
        """
        config_info = (
            f"Logger Configuration:\n"
            f" - Log Folder: {self.log_folder}\n"
            f" - Log File: {self.log_file}\n"
            f" - Log Level: {logging.getLevelName(self.log_level)}\n"
            f" - Log Backup Count: {self.log_backup}\n"
            f" - Max Bytes: {self.max_bytes} bytes"
        )
        print(config_info)


if __name__ == "__main__":
    # Initialize the EasyLog with default parameters
    easylog = EasyLog()
    logger = easylog.get_logger()

    # Display the current logger configuration
    easylog.show_logger_config()

    # Example log messages
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # Simulate an uncaught exception
    try:
        x = 1 / 0
    except Exception as e:
        logger.error("An exception occurred", exc_info=True)
