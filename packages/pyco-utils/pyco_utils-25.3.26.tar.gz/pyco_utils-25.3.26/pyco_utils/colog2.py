import os
import sys
import datetime
import logging
from pprint import pformat
from .co_shutil import safely_make_pardirs
from .colog import getLogger

##############################################################
##############################################################

NowStr = lambda fmt="%Y-%m-%d_%H%M": datetime.datetime.now().strftime(fmt)


class K():
    ## default options
    PYCO_LOGGER_NAME = "pyco"
    PYCO_LOGGER_LEVEL = logging.INFO
    PYCO_LOGFILE_DIR = "./logs"
    PYCO_LOGFILE_EXT = os.environ.setdefault("PYCO_LOGFILE_EXT", f".log")


glogger = logging.RootLogger(logging.INFO)


class PycoLogger2(logging.Logger):
    """ ##; usage_sample
    >>> from pyco_utils.colog2 import PycoLogger2
    >>> x = PycoLogger2()
    >>> x._logfile
    ;;; 'pyco.P87185.log'
    >>> x.__class__
    ;;; <class 'pyco_utils.colog2.PycoLogger2'>
    >>> isinstance(x, logging.Logger)
    ;;; True
    """
    _type = "PycoLogger2"
    _logfile = ""
    _stdout = True
    _kwargs = {}
    _pool = {}
    _env_k = "PYCO_LOGFILE"

    def __new__(__class__, logger_name="pyco", level=logging.INFO,
                set_as_global=False, logdir=K.PYCO_LOGFILE_DIR,
                logfile=None,
                stdout=True, **extra_kwargs
                ):
        kwargs = dict(locals())
        logger = __class__._pool.get(logger_name, None)
        if logger is not None:
            return logger
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        if logfile is None:
            log_fn = os.path.basename(logger_name).rsplit(".", 1)[0]
            logfile0 = f"{log_fn}.P{os.getpid()}.{K.PYCO_LOGFILE_EXT}".replace("..", ".")
            logfile = os.environ.setdefault(__class__._env_k, logfile0)
        elif isinstance(logfile, str):
            if not logfile.endswith(K.PYCO_LOGFILE_EXT):
                logfile = f"{logfile}.{K.PYCO_LOGFILE_EXT}"
        else:
            raise TypeError("$logfile must be a string.")
        safely_make_pardirs(logfile)
        logger = getLogger(logger_name, logfile=logfile, stdout=stdout, logdir=logdir, **kwargs)
        
        ## NOTE: 
        setattr(logger, "_logfile", logfile)
        setattr(logger, "_stdout", stdout)
        setattr(logger, "_kwargs", kwargs)
        logger.__class__ = __class__
        
        __class__._pool[logger_name] = logger
        logger.info(f"INIT logger({logger_name}): {logfile}")
        return logger

    def __init__(self, logger_name="pyco", level=logging.INFO, **kws):
        super(PycoLogger2, self).__init__(logger_name, level)


def get_logger2(logger_name="pyco", level=logging.INFO, set_as_global=False, logfile=None,
                stdout=True, **kwargs
                ):
    logger2 = PycoLogger2(
        logger_name,
        level=level,
        logfile=logfile,
        stdout=stdout,
        **kwargs
    )
    if set_as_global:
        global glogger
        glogger = logger2

    return logger2


def log(*args, stacklevel=2, log_level=50, **kwargs):
    # _log(*args, **kwargs, logger_name=logger.name, level=50, stacklevel=3)
    # logger = getLogger(logger_name, **kwargs)
    result = kwargs.pop('result', None)
    sep = "\t"
    msg = sep.join(map(str, args))
    if kwargs:
        msg += "\n" + pformat(kwargs, indent=2, width=120)
    if result is not None:
        msg += '\n[result] : \n\t{}'.format("\n\t".join(result.split("\n")))
    if sys.version_info > (3, 8, 0):
        ## Changed in version 3.8: The stacklevel parameter was added.
        glogger.log(log_level, msg, stacklevel=stacklevel)
    else:
        glogger.log(log_level, msg)


####################################################
####################################################
def _print_log(*args, **kwargs):
    print(*args, kwargs)


def _glogger_print_log(logger_name=K.PYCO_LOGGER_NAME):
    if logger_name:
        try:
            global glogger
            if glogger.name != logger_name:
                glogger = get_logger2(logger_name, set_as_global=True)

            def _print_log2(*args, stacklevel=4, **kwargs):
                log(*args, **kwargs, stacklevel=stacklevel)

            global _print_log
            _print_log = _print_log2
            _print_log(f"init Logger: {glogger.name} ({glogger.__class__.__name__})")
        except Exception as e:
            print(f"_get_print_log({logger_name}) failed", e)

# print(id(_print_log))
# _reset_print_log()
# print(id(_print_log))
