import os
import sys
import logging
from pprint import pformat
from datetime import datetime


class K():
    DISABLE_PRINT_LOG = bool(
        str(os.environ.get("DISABLE_PRINT_LOG", "0")).lower()
        in ["1", "yes", "true"]
    )


def time_string(ts_or_dt=None, format="%Y%m%d%_H%M%S"):
    if isinstance(ts_or_dt, (int, float)):
        dt = datetime.fromtimestamp(ts_or_dt)
    elif isinstance(ts_or_dt, datetime):
        dt = ts_or_dt
    elif isinstance(ts_or_dt, str):
        return ts_or_dt
    else:
        dt = datetime.now()
    return dt.strftime(format)


### NOTE: disable print_log in stable production environment  
### 这样的做的好处是, 判断是否使用 print_log 的 O(if-else)=1
if K.DISABLE_PRINT_LOG:
    print_log = lambda *args, **kws: 0
    print("[info] print_log is disabled !!! ($ENV.DISABLE_PRINT_LOG={} )".format(K.DISABLE_PRINT_LOG))
else:
    def print_log(*args, now=None, file=None, **kwargs):
        msg = " ".join(map(str, args))
        logger = kwargs.pop("logger", file)
        if kwargs:
            msg += "\r\n".join(pformat(kwargs, indent=2))
        if isinstance(logger, logging.Logger):
            logger.info(msg)
        else:
            if now is None:
                now = time_string()
            text = f"[{now}] {msg}"
            if file is None:
                print(text)
            elif getattr(file, "closed", None) == False:
                print(text, file=file)
                file.flush()
                if kwargs.get("stdout"):
                    print(f"WARN! unknown file=({type(file)}){file}")
                print(text, file=file)


def import_file(py_file, module_name=None, nullable=False, logger=None):
    # eg1: x = reload_py_file("your/path/x.py")
    # eg2: x3 = reload_py_file("your/path/x.py", "x2")
    import importlib
    import importlib.util

    if not module_name:
        module_name = os.path.basename(py_file).rstrip(".py").replace(".", "_")

    print_log("[todo] import_py_file: ", py_file, module_name, logger=logger)
    if not os.path.isfile(py_file):
        print_log("NOT FOUND:", py_file, logger=logger)
        if nullable:
            return None
        raise FileNotFoundError(py_file)

    imp_prev = sys.modules.get(module_name, None)
    if imp_prev is not None:
        fn_prev = "backup: {}._prev".format(module_name)
        print_log("backup module:", fn_prev, imp_prev, logger=logger)
        sys.modules[fn_prev] = imp_prev

    imp_spec = importlib.util.spec_from_file_location(module_name, py_file)
    if imp_spec is not None:
        py_imp = imp_spec.loader.load_module()
        print_log("reset sys.module:", module_name, py_imp, logger=logger)
        sys.modules[module_name] = py_imp
        return py_imp
    elif not nullable:
        print_log("ImportError", module_name, py_file, logger=logger)
        raise ImportError("{} => {}".format(module_name, py_file))
    else:
        print_log("ImportFailed", module_name, py_file, logger=logger)
        return None


def reload_module(py_module_dir, module_name=None, auto_init=True, nullable=False, logger=None):
    # eg1: x = reload_py_file("your/path/x")
    # eg2: x3 = reload_py_file("your/path/x", "x2")
    import importlib
    import importlib.util
    from datetime import datetime as DT

    if not os.path.exists(py_module_dir):
        if nullable:
            return None
        raise FileNotFoundError(py_module_dir)
    elif os.path.isdir(py_module_dir):
        py_module_init = os.path.join(py_module_dir, "__init__.py")
        py_module_init = os.path.abspath(py_module_init)
        if not os.path.exists(py_module_init):
            if auto_init:
                print_log("auto create: ", py_module_init, logger=logger)
                now_str = DT.now()
                with open(py_module_init, "w") as fw:
                    fw.write("# coding:utf-8")
                    fw.write("## auto created @ {}".format(now_str))
                    fw.write("## created by pyco-utils.reload_module({})".format(py_module_dir))
            else:
                print_log("Python Module missing __init__.py", py_module_dir, logger=logger)
                raise FileNotFoundError(py_module_init)
    else:
        # if os.path.isfile(py_module_dir)
        if not py_module_dir.endswith(".py"):
            print_log("warning: {} is not a python file".format(py_module_dir), logger=logger)
        py_module_init = py_module_dir

    py_module_dir = os.path.abspath(os.path.dirname(py_module_init))
    if py_module_dir != os.path.abspath(sys.path[0]):
        sys.path.insert(0, py_module_dir)
    try:
        imp_module = import_file(py_module_init, module_name=module_name, nullable=nullable)
        return imp_module
    except Exception as e:
        if not nullable:
            print_log("ImportError", module_name, py_module_init, logger=logger)
            raise e
        else:
            print_log("ImportFailed", module_name, py_module_init, logger=logger)
            return None


def clean_module(py_module_name, logger=None):
    sys_items = dict(sys.modules)
    py_file = getattr(py_module_name, "__file__", "")
    for k, v in sys_items.items():
        fp2 = getattr(v, "__file__", "")
        if fp2 == py_file:
            print_log("[clean_module]", k, v, logger=logger)
            sys.modules.pop(k, None)
            del v
            return True
    return False


def clean_modules_from_dir(py_module_dir, logger=None, suffix="_pb2", prefix=""):
    result = {}
    sys_items = dict(sys.modules)
    for k, v in sys_items.items():
        fp2 = getattr(v, "__file__", "")
        if (bool(suffix) and k.endswith(suffix)) or (bool(prefix) and k.startswith(prefix)):
            if fp2.startswith(py_module_dir):
                print_log("[-sys.module]", k, v, logger=logger)
                sys.modules.pop(k, None)
                del v
                result[k] = fp2
        elif fp2 == py_module_dir:
            sys.modules.pop(k, None)
            result[k] = fp2
    return result
