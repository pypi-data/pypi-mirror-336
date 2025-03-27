import io
import os
import sys
import time
import string
import random
import hashlib
from hashlib import md5
from datetime import datetime
from collections import OrderedDict

better_charset = 'abcdefghjkmnpqrstuvwxyz'  # !iol
hash_available = sorted(hashlib.algorithms_available)

NowStr = lambda fmt="%Y-%m-%d_%H%M": datetime.now().strftime(fmt)


def get_current_info(**kwargs):
    now = datetime.now()
    info = OrderedDict(
        _cwd=os.getcwd(),
        _pid=os.getpid(),
        _ppid=os.getppid(),
        _python_path=sys.executable,
        _python_version=sys.version,
        _sys_args=list(sys.argv),
        _created_at=str(now),
        _created_ts=int(time.time())
    )
    info.update(kwargs)
    return info


def md5sum(content):
    m = md5()
    if not isinstance(content, bytes):
        content = content.encode('utf-8').strip()
    m.update(content)
    s = m.hexdigest().lower()
    return s


def short_uuid(length):
    charset = string.ascii_letters + string.digits
    return ''.join([random.choice(charset) for i in range(length)])


def ts_rnd_key(size=4, fmt=".%y%m%d%H%M%S"):
    ts = datetime.now().strftime(fmt)
    rnd = ''.join(random.choice(better_charset) for i in range(size))
    return f'{ts}{rnd}'


def check_mkdir_depth(dir_path):
    ## 检查一个目录的创建深度，如果为 0，则为已经创建
    ## return: (int: 要创建的目录层级, str: 最临近的已存在的父级目录)
    dst = os.path.abspath(dir_path)
    if os.path.exists(dst):
        return 0, dst
    cnt = 1
    pdir = os.path.dirname(dst)
    while not os.path.exists(pdir):
        pdir2 = os.path.dirname(pdir)
        if pdir == pdir2:
            return cnt, None
        else:
            cnt += 1
            pdir = pdir2
    return cnt, pdir


def ensure_path(path, limit_depth=-1):
    if not os.path.exists(path):
        if limit_depth > 0:
            cnt, pdir = check_mkdir_depth(path)
            if cnt > limit_depth:
                raise NotADirectoryError(40490, path, f"pdir={pdir}, depth={cnt}>{limit_depth}")
        elif limit_depth == 0:
            raise NotADirectoryError(40490, path, f"limit_depth={limit_depth}")
        os.makedirs(path)


def get_pardir_of_path(path, depth=1):
    """
    usage: index to source and add to sys.path
    >>> folder = get_pardir_of_path(__file__, 1)
    >>> sys.path.insert(0, folder)
    """
    path = os.path.abspath(path)
    for i in range(depth):
        path = os.path.dirname(path)
    return path


def get_suffix_num(word: str):
    if not word[-1].isdigit():
        return -1
    elif word.isdecimal():
        return int(word)
    cnt = len(word)
    idx = cnt - 1
    plus = 1
    value = 0
    while word[idx].isdigit() and idx > 0:
        value += int(word[idx]) * plus
        plus *= 10
        idx -= 1
    return value


def _get_hasher(algorithm="md5"):
    # algo = getattr(hashlib, algorithm)
    # if not callable(algo):
    if algorithm not in hash_available:
        raise ValueError(f'Invalid hash({algorithm}),available: {hash_available}')
    algo = getattr(hashlib, algorithm)
    hasher = algo()
    return hasher


def hash_file(filename_or_fp, algorithm='sha256'):
    '''
    :param filename_or_fp: filename or file_stream buffered in binary mode
    :param algorithm: always support algorithms :
        'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
        'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
        'md5', 'blake2b', 'blake2s','shake_128', 'shake_256'
    :return: hash string

    :eg:
        m = hash_file('readme.md')

        f0 = open('readme.md')
        m0 = hash_file(f)
        # m == m0

        f1 = open('readme.md', encoding='utf-8')
        m1 = hash_file(f1)
        # m == m1

        f2 = open('readme.md', 'rb')
        m2 = hash_file(f2)
        # m == m2
    '''
    # sometimes you won't be able to fit the whole file in memory
    hasher = _get_hasher(algorithm)
    if isinstance(filename_or_fp, str) and os.path.isfile(filename_or_fp):
        with open(filename_or_fp, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                # print(len(chunk))
                hasher.update(chunk)
    elif isinstance(filename_or_fp, io.IOBase):
        filename_or_fp.seek(0)
        for chunk in iter(lambda: filename_or_fp.read(4096), b""):
            if (len(chunk) > 0):
                if not isinstance(chunk, bytes):
                    chunk = chunk.encode('utf-8')
                hasher.update(chunk)
            else:
                break
        filename_or_fp.seek(0)
    else:
        raise TypeError(f"Require FilePath or An Opened FileObject. Invalid $filename_or_fp=({filename_or_fp})")

    return hasher.hexdigest()
