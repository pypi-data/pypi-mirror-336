import os
import sys
from datetime import datetime
from pathlib import Path
from itertools import islice


class PathTree():
    space = '    '
    branch = '│   '
    tee = '├── '
    tail = '└── '


    @classmethod
    def _iter_dir(cls, dir_path: Path, level: int = -1, limit_to_directories: bool = False,
                  length_limit: int = 100, prefix: str = ""
                  ):
        """Given a directory Path object print a visual tree structure"""
        # accept string coerceable to Path
        dir_path = Path(dir_path)
        cnt_file = 0
        cnt_dir = 0
        cnt_level = level

        def inner(dir_path: Path, prefix: str = "", level=-1):
            nonlocal cnt_file, cnt_dir, cnt_level
            cnt_level = min(cnt_level, level)
            if not level:
                return  # 0, stop iterating
            contents = list(dir_path.iterdir())
            pointers = [cls.tee] * (len(contents) - 1) + [cls.tail]
            for pointer, path in zip(pointers, contents):
                if path.is_dir():
                    yield prefix + pointer + path.name
                    cnt_dir += 1
                    extension = cls.branch if pointer == cls.tee else cls.space
                    yield from inner(path, prefix=prefix + extension, level=level - 1)
                elif not limit_to_directories:
                    yield prefix + pointer + path.name
                    cnt_file += 1

        yield dir_path.name
        iterator = inner(dir_path, prefix=prefix, level=level)
        for line in islice(iterator, length_limit):
            yield line
        if next(iterator, None):
            yield f'{prefix}...more...'
        total = cnt_file + cnt_dir
        yield f'\n\n###> {cnt_dir} directories, {cnt_file} files\n' \
              f'#### access:{total}, length_limit:{length_limit}, ' \
              f'depth_limit:{level}, ' \
              f'depth_reached:{level - cnt_level} '


    @classmethod
    def tree_txt(cls, dir_path: str, **kwargs):
        if not isinstance(dir_path, Path):
            dir_path = Path(dir_path)
        text = "\n".join(cls._iter_dir(dir_path, **kwargs))
        return text


def print_tree(dir_path: str, **kwargs):
    dir_path = Path(dir_path)
    dir2 = os.path.abspath(dir_path)
    print(f"#### abs: {dir2} ")
    t1 = datetime.now()
    print(f"#### start: {t1} ")
    for line in PathTree._iter_dir(dir_path, **kwargs):
        print(line)
    t2 = datetime.now()
    print(f"#### finished: {t2}, spend: {t2 - t1}")


def tree_txt(dir_path: str, **kwargs):
    return PathTree.tree_txt(dir_path, **kwargs)


if __name__ == '__main__':
    # tree_std(".", prefix="   ", length_limit=500, level=2)
    print(sys.path)
    print(os.environ)
    dir_path = "."
    if len(sys.argv) > 2:
        dir_path = sys.argv[-1]
    print_tree(dir_path)
