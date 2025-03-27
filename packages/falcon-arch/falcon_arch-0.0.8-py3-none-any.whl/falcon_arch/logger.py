import logging
import sys

# Define custom log levels
INFO_LEVEL = logging.INFO
SUCCESS_LEVEL = logging.INFO
WARNING_LEVEL = logging.WARNING
ERROR_LEVEL = logging.ERROR
CRITICAL_LEVEL = logging.CRITICAL
DEBUG_LEVEL = logging.DEBUG
TIME_LEVEL = 25

# Add custom names for the levels
logging.addLevelName(INFO_LEVEL, "📢")
logging.addLevelName(SUCCESS_LEVEL, "✅")
logging.addLevelName(WARNING_LEVEL, "🚨")
logging.addLevelName(ERROR_LEVEL, "❌")
logging.addLevelName(CRITICAL_LEVEL, "🚫")
logging.addLevelName(DEBUG_LEVEL, "🐛")
logging.addLevelName(TIME_LEVEL, "⏳")

class Logger:
    @staticmethod
    def setup(level: int = INFO_LEVEL, datefmt = "%d/%m/%Y %H:%M:%S", log_file=None):
        """
        Configures the logging system.
        """
        if logging.getLogger().hasHandlers():
            return

        handlers = [logging.StreamHandler(sys.stdout)]
        
        if log_file:
            handlers.append(logging.FileHandler(log_file, mode='a', encoding='utf-8'))

        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt=datefmt,
            handlers=handlers
        )

    @staticmethod
    def info(message: str, service: str = None):
        Logger.___log(INFO_LEVEL, message, service)

    @staticmethod
    def success(message: str, service: str = None):
        Logger.___log(SUCCESS_LEVEL, message, service)

    @staticmethod
    def warning(message: str, service: str = None):
        Logger.___log(WARNING_LEVEL, message, service)

    @staticmethod
    def error(message: str, service: str = None):
        Logger.___log(ERROR_LEVEL, message, service)

    @staticmethod
    def debug(message: str, service: str = None):
        Logger.___log(DEBUG_LEVEL, message, service)

    @staticmethod
    def time(message: str, service: str = None):
        Logger.___log(TIME_LEVEL, message, service)

    @staticmethod
    def ___log(level: int, message: str, service: str = None):
        if service:
            message = f"{service}: {message}"

        if logging.getLogger().isEnabledFor(level):
            logging.log(level, message)
