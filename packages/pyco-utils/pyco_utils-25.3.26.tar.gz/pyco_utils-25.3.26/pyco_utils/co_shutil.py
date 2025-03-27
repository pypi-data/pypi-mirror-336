import os
import shutil

from .__adapt import check_mkdir_depth
from ._subproc import run_subprocess, PycoTaskStatusTP
from ._coimp import time_string


class K():
    auto_mkdir_limit_depth = 4
    failed_logfile = "logs/_pyco_failed.txt"
    log_if_move_file_failed = True
    exception_if_remove_fail = True
    global_ignored_tags = [".bak.", "@tmp", "backup@", "tmp@", "outputs@bak", "output@", "logs"]


    @classmethod
    def add_errmsg(cls, cmd="", tips=""):
        with safely_open(cls.failed_logfile, "a+") as fw:
            now_str = time_string()
            tag1 = f"\r\n#{now_str} @{os.getpid()} {os.getuid()}\r\n"
            fw.write(tag1)
            if tips:
                tag2 = f'echo "{tips}"'
                fw.write(tag2)
            msg1 = cmd + " " + os.linesep
            fw.write(msg1)

    @staticmethod
    def find_text_key(text: str, key: str, sep="/",
                      ignore_case=True, offset=1,
                      enable_suffix=True,
                      enable_prefix=True,
                      enable_include=False,
                      **kws
                      ):
        """
        eg1: ("a1j.2.proto.imu", "proto", ".") => "imu"
        eg2: ("A1J.2.PROTO.IMU", "proto", ".", offset=-2) => "A1J" 
        eg2: ("A1J.2.PROTO.IMU", "IMU", ".") => "A1J"
        eg2: ("A1J.2.PROTO.IMU", "imu", ".", ignore_case=False) => "" 
        """
        ps = list(filter(lambda x: bool(x), text.split(sep)))
        cnt = len(ps)
        for i, p in enumerate(ps):
            if p == key:
                return ps[(i + offset) % cnt]
            if ignore_case:
                p = p.lower()
                if p == key.lower():
                    return ps[(i + offset) % cnt]
            if enable_suffix and p.endswith(key):
                return ps[(i + offset) % cnt]
            if enable_prefix and p.startswith(key):
                return ps[(i + offset) % cnt]
            if enable_include and (key in p):
                return ps[(i + offset) % cnt]
        return ""


    @classmethod
    def is_ignorable_path(cls, text: str, ignored_keys=None, strict=False, sep="/", **kws):
        # (output.bak.yymmdd, [".bak.", "@bak"]
        text = text.strip()
        if isinstance(ignored_keys, str):
            ignored_keys = [ignored_keys]
        elif ignored_keys is None:
            ignored_keys = cls.global_ignored_tags
        if text in ignored_keys:
            return True
        if not strict:
            for k in ignored_keys:
                k2 = k.strip()
                if k2:
                    v2 = cls.find_text_key(
                        text, k2, sep=sep, offset=0,
                        ignore_case=True,
                        enable_include=True,
                        enable_prefix=True,
                        enable_suffix=True,
                    )
                    if v2:
                        return True
        return False


def _generate_pardir_from_seed(fp_path, limit=1, subdir=".git"):
    ## 在 $fp_path 的父级目录中，过滤生成包含 $subdir 的父目录
    fn = os.path.abspath(fp_path)
    if os.path.isdir(fn):
        p = fn
    else:
        p = os.path.dirname(fn)
    while limit:
        p2 = os.path.join(p, subdir)
        if os.path.isdir(p2):
            limit -= 1
            yield p
        p3 = os.path.dirname(p)
        if p3 == p:
            limit = 0
        else:
            p = p3


def find_up_pardir(fp_path, subdir=".git"):
    ## 从子路径，往上查找父路径，找到距离 $fp_path 层级最近的，且包括 $subdir 的父目录
    _gen = _generate_pardir_from_seed(fp_path, limit=1, subdir=subdir)
    ps = list(_gen)
    if len(ps) > 0:
        return ps[0]


def cover_file(src, dst, **kwargs):
    ### src, dst 是已经存在的文件路径（绝对路径）
    cmd1 = f"cat {src} > {dst}"
    res1 = run_subprocess(cmd1)
    if res1.code == 0:
        try:
            os.remove(src)
            msg = f"覆盖成功（{dst}），已删除源文件：{src}"
            print(msg)
            return PycoTaskStatusTP(0, msg)
        except Exception as e:
            msg = f"覆盖成功（{dst}），但是无法删除源文件：{src}"
            cmd2 = f"rm {src}"
            K.add_errmsg(cmd2, tips=msg)
            print(msg, e)
            if K.exception_if_remove_fail:
                raise e
            else:
                return PycoTaskStatusTP(2, msg)
    return res1


def safely_make_pardirs(dst, auto_mkdir_limit_depth=K.auto_mkdir_limit_depth, **kwargs):
    pdir = os.path.dirname(dst)
    pdir_depth, pdir2 = check_mkdir_depth(pdir)
    if pdir_depth > 0:
        if pdir_depth <= auto_mkdir_limit_depth or auto_mkdir_limit_depth < 0:
            print(f"【创建父目录】：{pdir} ({pdir_depth}=>{pdir2})")
            os.makedirs(pdir)
        else:
            msg = f"#【父目录不存在】:({pdir_depth}=>{pdir2}), 访问失败：{dst}"
            print(msg)
            K.add_errmsg(tips=msg)
            raise NotADirectoryError(pdir)


def safely_open(output, mode="w", **kwargs):
    ## DONE: => pyco_utils.init
    ## auto_mkdirs: 0-不创建父目录；>0,限制深度创建父目录；<0, 无限深度创建父目录；
    safely_make_pardirs(output, **kwargs)
    if mode != "r":
        print(f"[TODO]save({mode}): {output}")
    return open(output, mode=mode, **kwargs)


def merge_subtree(src, dst, **kwargs):
    ## src,dst 必须是已经存在的绝对路径，且均为目录
    ss1 = os.listdir(src)
    if K.is_ignorable_path(src):
        msg=f"# merge_subtree({src}, {dst}), ignored!"
        K.add_errmsg(msg)       
        return
        
    for s1 in ss1:
        sd1 = os.path.join(src, s1)
        sd2 = os.path.join(dst, s1)
        if os.path.exists(sd2):
            if os.path.isfile(sd1):
                cover_file(sd1, sd2)
            else:
                merge_subtree(sd1, sd2)
        else:
            shutil.move(sd1, dst)



def safely_move_file(src, dst, **kwargs):
    ## src,dst 必须是已经存在的绝对路径，src必须是文件, dst 可能是目录
    try:
        dst2 = shutil.move(src, dst)
        return PycoTaskStatusTP(0, "move成功", data=dst2)
    except Exception as e:
        print(f'[Error] mv {src} {dst} \n{e}\n')
        src_bn = os.path.basename(src)
        if os.path.isdir(dst):
            dst2 = os.path.join(dst, src_bn)
            if os.path.isfile(dst2):
                return cover_file(src, dst2, **kwargs)
            else:
                if K.log_if_move_file_failed:
                    K.add_errmsg(f"mv {src} {dst}")
                raise e
        else:
            return cover_file(src, dst, **kwargs)


def pyco_move(src: str, dst: str, merge_if_dir_exist=True, **kwargs):
    """
    1. 如果是 mv
    """
    ## use os.path.abspath
    ## 如果子文件夹同名，且dst已经存在，
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)
    print(f"[TODO] pyco_move {src} {dst}")
    if not os.path.exists(src):
        errmsg = f"[Error] NotExist: {src}"
        return PycoTaskStatusTP(code=40460, msg=errmsg)

    ## 如果目标路径不存在，只要有写的权限，一般都能成功
    if not os.path.exists(dst):
        safely_make_pardirs(dst, **kwargs)
        dst2_ = shutil.move(src, dst)
        return PycoTaskStatusTP(data=dst2_)

    ## 如果目标路径已经存在，不一定有os.rename的权限，需要检查
    src_bn = os.path.basename(src)
    if os.path.isdir(src):
        if os.path.isdir(dst):
            dst2 = os.path.join(dst, src_bn)
            ### 如果两个都是目录，且dst2已经存在，会失败
            if not os.path.exists(dst2):
                dst2_ = shutil.move(src, dst)
                return PycoTaskStatusTP(data=dst2_)
            elif os.path.isdir(dst2):
                if merge_if_dir_exist:
                    print(f"[WARN] 已经存在目标路径: {dst2}, 即将开始merge_subtree")
                    return merge_subtree(src, dst2)
                else:
                    errmsg = f"[Error] 路径冲突，已经存在目标路径:({dst2}), 如果要 merge_subtree, 请使用`merge_if_dir_exist=True`"
                    return PycoTaskStatusTP(code=40962, msg=errmsg)
            elif os.path.isfile(dst2):
                errmsg = f"[Error] 路径冲突，已经存在目标文件:({dst2})，而源是一个目录:({src})"
                return PycoTaskStatusTP(code=40963, msg=errmsg)
        else:
            errmsg = f"[Error] 路径冲突，已经存在目标文件:({dst})，而源是一个目录:({src})"
            return PycoTaskStatusTP(code=40964, msg=errmsg)

    elif os.path.isfile(src):
        return safely_move_file(src, dst)
    