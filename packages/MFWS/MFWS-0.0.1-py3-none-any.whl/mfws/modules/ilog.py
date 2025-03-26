# 日志管理
import os
import os.path as o_p
import logging
import sys
import time
import io
from typing import Literal

PROG_VERSION = '0.1'
PROG_DATE = '2021-07-25'

usage = '''
Version %s  by Chen Bichao  %s
Usage: 
import stlog
ilog.log2file()

ilog.info("Test info.")
ilog.warning("Logging warning.")
''' % (PROG_VERSION, PROG_DATE)

# Logging levels
ROOT = logging.root
CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG

# create a dict for level name strings
level_name = {
    CRITICAL: "CRITICAL",
    ERROR: "ERROR",
    WARNING: "WARNING",
    INFO: "INFO",
    DEBUG: "DEBUG"
}

FMTDCIT = {
    '\033[31mERROR\033[0m': "ERROR",
    '\033[32mINFO\033[0m': "INFO",
    'DEBUG': "DEBUG",
    '\033[33mWARNING\033[0m': "WARNING",
    '\033[35mCRITICAL\033[0m': "CRITICAL",
}


# 此处修改颜色
COLOR_FMTDCIT = {
    'ERROR': "\033[31mERROR\033[0m",
    'INFO': "\033[32mINFO\033[0m",
    'DEBUG': "\033[1mDEBUG\033[0m",
    'WARNING': "\033[33mWARNING\033[0m",
    'CRITICAL': "\033[35mCRITICAL\033[0m",
}


class CMDFilter(logging.Filter):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def filter(self, record: logging.LogRecord) -> bool:
        record.levelname = COLOR_FMTDCIT.get(record.levelname)
        return True


class FileFilter(logging.Filter):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def filter(self, record: logging.LogRecord) -> bool:
        record.levelname = FMTDCIT.get(record.levelname)
        return True


cmd_filter = CMDFilter()
file_filter = FileFilter()


class CLogger(object):
    """ Custom logger class to format and instantiate logger. """
    file_handler = None

    def __init__(self, level: Literal[10, 20, 30, 40, 50] = INFO):
        """ Initialize logger, default logger has one StreamHandler. """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(DEBUG)
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setLevel(level)
        self.stream_handler.setFormatter(self.st_formatter())
        self.stream_handler.addFilter(cmd_filter)
        self.logger.addHandler(self.stream_handler)
        self.logfile = ''

    def log2file(self, out_dir='', filename='', level: Literal[10, 20, 30, 40, 50] = DEBUG):
        """ Save logging to file. """
        if len(self.logfile) == 0:
            self.logfile = self._set_logfile(out_dir, filename)
            # self.logger.info('Log file will store in {}'.format(out_dir))
            self.file_handler = logging.FileHandler(self.logfile, 'a')
            self.file_handler.addFilter(file_filter)
            self.file_handler.setLevel(level)
            # if not len(self.logger.handlers):
            self.file_handler.setFormatter(self.st_formatter())
            self.logger.addHandler(self.file_handler)
        else:
            print("log file is set.")
            print(self.logfile)

    @staticmethod
    def _set_logfile(out_dir='', filename=''):
        """ Set logging file. """
        if len(out_dir) == 0:
            out_dir = o_p.join(o_p.dirname(o_p.dirname(__file__.replace('\\', '/'))), 'log')
        os.makedirs(out_dir, exist_ok=True)

        if len(filename) == 0:
            filename = time.strftime("%Y%m%d-%H-%M-%S", time.localtime()) + '.log'
        return o_p.join(out_dir, filename)

    def get_logfile(self):
        """ Get current logging file. """
        for hdl in self.logger.handlers:
            if isinstance(hdl, logging.FileHandler):
                return hdl.baseFilename
        return ''

    @staticmethod
    def st_formatter():
        """ Logging formatter. """
        # Sample: [INFO 20210723-15:41:55 p12027 <module> stlog.py:153] This is a debug message
        fmt_str = "[%(levelname)s %(asctime)s p%(process)s %(funcName)s %(filename)s:%(lineno)s] %(message)s"
        return logging.Formatter(fmt=fmt_str, datefmt="%Y%m%d-%H-%M-%S", style='%')

    # def set_level(self,
    #               stream_level: Literal[10, 20, 30, 40, 50],
    #               file_level: Literal[10, 20, 30, 40, 50]):
    #     """ Set logger level. """
    #     try:
    #         self.file_handler.setLevel(file_level)
    #         self.stream_handler.setLevel(stream_level)
    #     except Exception as e:
    #         print(e)
    #     self.logger.debug("Logging level is set to (stream, file) == ({}, {})".format(
    #         level_name[stream_level], level_name[file_level]))


class TqdmToLogger(io.StringIO):
    """
        Output stream for TQDM which will output to logger module instead of
        the StdOut.
    """
    logger = None
    level = None
    buf = ''

    def __init__(self, logger, level=None):
        super(TqdmToLogger, self).__init__()
        self.logger = logger
        self.level = level or logging.INFO

    def write(self, buf):
        self.buf = buf.strip('\r\n\t ')

    def flush(self):
        self.logger.log(self.level, self.buf)


# Set logging methods
cl = CLogger()
logger = cl.logger

get_logfile = cl.get_logfile
log2file = cl.log2file
# set_level = cl.set_level
#
# # set logging base level to INFO
# set_level(INFO, file_level=DEBUG)

debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
tqdm_out = TqdmToLogger(logger)


if __name__ == "__main__":
    print(usage)
