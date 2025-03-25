import logging
import sys


class Logger:
    def __init__(self):
        """Initialize the logger"""
        self.logger = logging.getLogger("req-test-align")
        self.logger.setLevel(logging.INFO)

        # Create a console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # Create a formatter
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(formatter)

        # Add the handler
        self.logger.addHandler(console_handler)

        # Prevent duplicate logs
        self.logger.propagate = False

    def set_debug(self, debug: bool):
        """Set the debug mode"""
        if debug:
            self.logger.setLevel(logging.DEBUG)
            for handler in self.logger.handlers:
                handler.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
            for handler in self.logger.handlers:
                handler.setLevel(logging.INFO)

    def debug(self, message: str):
        """Log a debug message"""
        self.logger.debug(message)

    def info(self, message: str):
        """Log an info message"""
        self.logger.info(message)

    def warning(self, message: str):
        """Log a warning message"""
        self.logger.warning(message)

    def error(self, message: str):
        """Log an error message"""
        self.logger.error(message)

    def critical(self, message: str):
        """Log a critical message"""
        self.logger.critical(message)


# Create a global logger instance
logger = Logger()
