import time
from pprint import pformat
import threading
from functools import (
    wraps,
    reduce,
)

from ._format import pf_echo


def pf_time(func, logger=None):
    '''
    @log_time
    def func():
        pass
    '''
    t1 = time.time()

    @wraps(func)
    def wrapper(*args, **kwargs):
        m = func(*args, **kwargs)
        t2 = time.time()
        tm = t2 - t1
        msg = '{}, {}ms \n<{}>\n'.format(func.__name__, tm, pformat(m))
        print(msg)
        return m

    return wrapper


def ajax_func(func, daemon=True):
    @wraps(func)
    def wrapper(*args, **kwargs):
        th = threading.Thread(target=func, args=args, kwargs=kwargs)
        th.daemon = daemon
        th.start()

    return wrapper


def retry(func, count=3):
    '''
    @retry
    def func():
        pass
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        for i in range(count - 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(pf_echo(func, *args, **kwargs))
                print("[ERROR]: ", pformat(e))
        return func(*args, **kwargs)

    return wrapper


def retry_api(count=3, delay=30, exceptions=None):
    '''
    ##; usage sample:
    from urllib.error import HTTPError
    from werkzeug.exceptions import (
        TooManyRequests,
        GatewayTimeout,
        RequestTimeout,
    )

    exceptions = (
        HTTPError,
        RequestTimeout,
        GatewayTimeout,
        TooManyRequests,
    )

    @retry_api(exceptions=exceptions)
    def func():
        pass
    '''
    if exceptions is None:
        exceptions = Exception

    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(count - 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(pf_echo(func, *args, **kwargs, ERROR=e))
                    time.sleep(delay)

            return func(*args, **kwargs)

        return wrapper

    return deco
