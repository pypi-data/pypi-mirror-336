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

    _instance = None
    _logger = None

    # Class-level default parameters
    log_folder = "/tmp/out/easylog"
    log_file = "log.log"
    log_level = logging.INFO
    log_backup = 2
    max_bytes = 80 * 1024 * 1024

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to ensure only one instance of EasyLog is created.
        """
        if cls._instance is None:
            cls._instance = super(EasyLog, cls).__new__(cls)
            cls._initialize_logger()  # Initialize the logger automatically
        return cls._instance

    @classmethod
    def _initialize_logger(cls):
        """
        Internal method to initialize the logger with the specified class-level parameters.
        This method is called automatically when the instance is created.
        """
        if cls._logger is not None:
            return  # Logger is already initialized

        # Clear existing log files in the log folder
        if os.path.exists(cls.log_folder):
            for log_file in os.listdir(cls.log_folder):
                log_file_path = os.path.join(cls.log_folder, log_file)
                if os.path.isfile(log_file_path):
                    os.remove(log_file_path)

        # Create the log folder if it does not exist
        if not os.path.exists(cls.log_folder):
            os.makedirs(cls.log_folder)

        # Create the logger
        cls._logger = logging.getLogger(__name__)
        cls._logger.setLevel(cls.log_level)

        # Set up the file handler for logging to a file
        log_file_path = os.path.join(cls.log_folder, cls.log_file)
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=cls.max_bytes,
            backupCount=cls.log_backup,
            encoding="utf-8",
        )
        file_formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d - %(funcName)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        cls._logger.addHandler(file_handler)

        # Initialize colorama for colored console output
        init(autoreset=True)

        # Set up the console handler for logging to the terminal
        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter(
            "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d - %(funcName)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(console_formatter)
        cls._logger.addHandler(console_handler)

        # Set up an exception hook to log uncaught exceptions
        def log_exception(exc_type, exc_value, exc_traceback):
            cls._logger.error(
                "Uncaught exception",
                exc_info=(exc_type, exc_value, exc_traceback),
            )

        sys.excepthook = log_exception

    @classmethod
    def get_logger(cls):
        """
        Get the initialized logger instance.
        """
        if cls._logger is None:
            raise Exception(
                "Logger is not initialized. Please check the configuration."
            )
        return cls._logger

    @classmethod
    def show_logger_config(cls):
        """
        Display the current logger configuration.
        """
        config_info = (
            f"Logger Configuration:\n"
            f" - Log Folder: {cls.log_folder}\n"
            f" - Log File: {cls.log_file}\n"
            f" - Log Level: {logging.getLevelName(cls.log_level)}\n"
            f" - Log Backup Count: {cls.log_backup}\n"
            f" - Max Bytes: {cls.max_bytes} bytes"
        )
        print(config_info)


if __name__ == "__main__":
    # Set custom parameters for the logger (optional)
    EasyLog.log_folder = "/tmp/my_custom_logs"
    EasyLog.log_file = "custom_log.log"
    EasyLog.log_level = logging.DEBUG
    EasyLog.log_backup = 5
    EasyLog.max_bytes = 100 * 1024 * 1024

    # Get the logger instance (logger is initialized automatically)
    logger = EasyLog().get_logger()

    # Display the current logger configuration
    EasyLog.show_logger_config()

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
