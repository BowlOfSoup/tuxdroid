import logging
import sys

class Logger:

    def __init__(self):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='[%Y-%m-%d %H:%M:%S]')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter("%(asctime)s %(message)s")

    @staticmethod
    def _colored(level, message):
        colors = {
            'red': "\033[91m",
            'yellow': '\033[93m',
            'green': '\033[92m',
            'turquoise': '\033[96m',
            'reset': "\033[0m"
        }

        return colors[level] + message + colors['reset']

    def info(self, message):
        self.logger.info(self._colored('turquoise', message))

    def success(self, message):
        self.logger.info(self._colored('green', message))

    def warning(self, message):
        self.logger.warning(self._colored('yellow', message))

    def error(self, message):
        self.logger.error(self._colored('red', message))