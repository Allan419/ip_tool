import sys
import logging
from settings import LOG_LEVEL, LOG_FORMAT, LOG_DATEFMT, LOG_FILENAME, LOG_PROXY_SPIDER

class Logger(object):
    def __init__(self, log_filename):
        self._logger = logging.getLogger()
        self.formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATEFMT)
        self._logger.addHandler(self._get_file_handler(log_filename))
        self._logger.addHandler(self._get_console_handler())
        self._logger.setLevel(LOG_LEVEL)

    def _get_file_handler(self, filename):
        file_handler = logging.FileHandler(filename=filename, encoding='utf-8')
        file_handler.setFormatter(self.formatter)
        return file_handler

    def _get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    @property
    def logger(self):
        return self._logger

logger = Logger(LOG_FILENAME).logger
loggerProxySpider = Logger(LOG_PROXY_SPIDER).logger

if __name__ == '__main__':
    logger.debug("调试信息")
    logger.info("状态信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.critical("严重错误信息")

    

