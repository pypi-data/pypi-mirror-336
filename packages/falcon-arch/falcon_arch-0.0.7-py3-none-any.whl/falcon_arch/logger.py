import logging
import sys

TIME_LEVEL = 25
logging.addLevelName(TIME_LEVEL, "TIME")

class Logger:
    @staticmethod
    def setup(level=logging.INFO, log_file=None):
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
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=handlers
        )

        logging.info("✔️  Logging setup completed.")

    @staticmethod
    def info(message: str):
        """
        Logs an info message.

        :param message: Main log message.
        """
        logging.info(f"📢 {message}")

    @staticmethod
    def success(message: str, service: str = None, duration: float = None):
        """
        Logs a success message.

        :param message: Main log message.
        :param service: (Optional) Name of the service or component.
        :param duration: (Optional) Execution time in seconds.
        """
        log_message = f"✅ {message}"
        
        if service:
            log_message = f"✅ {service}: {message}"
        
        if duration is not None:
            log_message += f" in {duration:.4f} seconds."
        
        logging.info(log_message)

    @staticmethod
    def warning(message: str, service: str = None):
        """
        Logs a warning message.

        :param message: Main log message.
        :param service: (Optional) Name of the service or component.
        """
        log_message = f"🚨 {message}"
        
        if service:
            log_message = f"🚨 {service}: {message}"
        
        logging.warning(log_message)

    @staticmethod
    def error(message: str):
        """
        Logs an error message.

        :param message: Main log message.
        """
        logging.error(f"❌ {message}")

    @staticmethod
    def debug(message: str, service: str = None):
        """
        Logs a debug message.

        :param message: Main log message.
        :param service: (Optional) Name of the service or component.
        """
        log_message = f"🐛 {message}"
        
        if service:
            log_message = f"🐛 {service}: {message}"
        
        logging.debug(log_message)

    @staticmethod
    def time(message: str):
        """
        Logs a time-related message.

        :param message: Main log message.
        """
        if logging.getLogger().isEnabledFor(TIME_LEVEL):
            logging.log(TIME_LEVEL, f"⏳ {message}")
