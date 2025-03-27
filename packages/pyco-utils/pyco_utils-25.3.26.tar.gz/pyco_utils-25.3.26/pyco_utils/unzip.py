import os
import io
import shutil
import zipfile
from datetime import datetime
from .__adapt import short_uuid
__MACOSX = '__MACOSX'


def fp_mtime(fp: str, fmt='%Y%m%d%H%M'):
    return datetime.fromtimestamp(os.stat(fp).st_mtime).strftime(fmt)


def sink_dir(dir_path, limit=-1, ignore_macosx=True):
    """
    ## 定位被嵌套于单目录的单目录, 默认无限
    f = "a/bb/ccc/dddd/eeeee/ffffff"
    os.makedirs(f)
    f1 = sink_dir("a", limit=1)  ##  => "a/bb"
    f2 = sink_dir("a", limit=2)  ##  => "a/bb/ccc"
    f3 = sink_dir("a")           ##  => "a/bb/ccc/dddd/eeeee/ffffff"
    """
    subs = os.listdir(dir_path)
    if ignore_macosx and (__MACOSX in subs):
        subs.remove(__MACOSX)
        print(f'ignore {__MACOSX}: {dir_path}')

    if len(subs) == 1:
        subdir = os.path.join(dir_path, subs[0])
        if os.path.isdir(subdir):
            if limit:
                print(f"seek => {subdir}")
                return sink_dir(subdir, limit - 1, ignore_macosx)
    return dir_path


def extract_all(src_path, dst_dir, auto_backup=True, ignore_macosx=True, sink_limit=-1):
    """
    ## 把zip包解压到指定目录中, 通常用于支持发布包管理
    ## 我们期待的结果是: dst_dir 目录下至少有一个文件file 或 两个子目录dir
    ## 如果是解压后得到是单个文件夹(dir), 需要把路径下沉1级, 通常由 MacOs打包所触发
    Args:
       src_path: str: zip 源文件的路径
       dst_dir: str: 输出目录, 要求为空目录, 应当在调用时, 确保它的上层目录存在
       auto_backup: bool(True): 如果 dst_dir 不是空目录, 是否要自动备份
       ignore_macosx: bool(True): 是否忽略 MacOs 压缩文件所产生的 __MACOSX
    """
    if os.path.exists(dst_dir):
        if len(os.listdir(dst_dir)) > 0:
            if auto_backup:
                dst_bak = '{}.bak.{}'.format(dst_dir, fp_mtime(dst_dir))
                os.rename(dst_dir, dst_bak)

    ## 创建临时解压目录
    dst_tmp = "{}.tmp.{}".format(dst_dir, short_uuid(4))
    with zipfile.ZipFile(src_path, "r") as fp:
        fp.extractall(dst_tmp)

    ## 不同的压缩工具对打包单个文件夹, 有不同的实现
    ## 如果是解压后得到是单个文件夹(dir), 需要把路径下沉1级, 通常由 MacOs打包所触发
    dst_tmp2 = sink_dir(dst_tmp, sink_limit, ignore_macosx=ignore_macosx)
    if dst_tmp2 == dst_tmp:
        os.rename(dst_tmp, dst_dir)
        print('mv', dst_tmp, dst_dir)
    else:
        os.rename(dst_tmp2, dst_dir)
        shutil.rmtree(dst_tmp)
        # os.rmdir(dst_tmp)
        print('cp', dst_tmp2, dst_dir)
        print('rm', dst_tmp)
    return True
