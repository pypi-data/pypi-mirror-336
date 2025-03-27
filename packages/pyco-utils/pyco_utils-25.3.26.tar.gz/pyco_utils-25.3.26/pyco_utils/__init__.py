import os
import sys

__version__ = '25.3.26'
__module_name = "pyco_utils"

## fixed: 避免覆盖标准库（_json）
_curdir_ = os.path.abspath(os.path.dirname(__file__))
if _curdir_ in sys.path:
    sys.path.remove(_curdir_)

from .__adapt import (
    hash_file,
    md5sum,
    short_uuid,
    ts_rnd_key,
    check_mkdir_depth,
    ensure_path,
    get_pardir_of_path,
    get_suffix_num,
)
from ._coimp import (
    print_log,
    reload_module,
    import_file,
    clean_module,
    clean_modules_from_dir,
)

from . import (
    __adapt,
    _json,
    _coimp,
    _compat,
    _format,
    _subproc,
    co_shutil,
    colog,
    decorators,
    form_data,
    reverify,
    const,
)

# from . import _json
## fixed: compat with _json.cpython on python>=3.7  
sys.modules["pyco_utils._json"] = _json
