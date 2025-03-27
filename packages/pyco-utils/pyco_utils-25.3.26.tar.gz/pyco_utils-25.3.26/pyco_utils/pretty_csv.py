import os


def str_limit_size(s: str, prefix=6, suffix=8, max_size=20):
    if len(s) > max_size:
        return f'{s[:prefix]}...{s[-suffix:]}'
    return s


def align_dict_items(dmap: dict, padding=2, sep="-", __fillchar="&nbsp;"):
    ## 对齐 dict.items() 的长度, 使分隔符 对齐
    cl = 0
    cr = 0
    for k, v in dmap.items():
        cl = max(cl, len(str(k)))
        cr = max(cr, len(str(v)))
    res = {}
    for k, v in dmap.items():
        # res[k] = f"{k}{space * (cl + padding - len(str(k)))}{sep}{space * (cr + padding - len(str(v)))}{str(v)}"
        sk = str(k).ljust(cl + padding, __fillchar=__fillchar)
        sv = str(v).ljust(cr + padding, __fillchar=__fillchar)
        res[k] = f"{sk}{sep}{sv}"
    return res


class CsvPrettier():
    _fillchar = " "
    _max_col_size = 120
    _cols_sep = " , "
    _line_sep = os.linesep
    _padding = 0

    def __init__(self, Array2D: list, set_row_id=True, cnt_cols=0):
        self._Array2D = Array2D  ##List: [[...cols]]
        self._cnt_rows = len(Array2D)
        self._cnt_cols = cnt_cols
        if cnt_cols == 0 and self._cnt_rows > 0:
            self._cnt_cols = len(Array2D[0])
        self._ary_of_col_msz = [0 for i in range(self._cnt_cols)]
        self.__x_ary_of_col_msz = False
        self._cur_id = 0
        self.set_row_id = set_row_id


    @property
    def ary_of_col_msz(self):
        # array of column max size
        if not self.__x_ary_of_col_msz:
            for i in range(self._cnt_cols):
                col_max = max(map(lambda x: len(str(x[i])), self._Array2D))
                self._ary_of_col_msz[i] = max(col_max, self._max_col_size)
            self.__x_ary_of_col_msz = True
        return self._ary_of_col_msz


    def _pretty_row(self, row):
        ps = []
        self._cur_id += 1
        if self.set_row_id:
            ps.append(str(self._cur_id))
        col_msz = self.ary_of_col_msz
        for i, v in enumerate(row):
            p = str(v).ljust(col_msz[i] + self._padding, self._fillchar)
            ps.append(p)
        line = self._line_sep.join(ps)
        return line

    def pretty_content(self):
        lines = []
        for _i, row in enumerate(self._Array2D):
            line = self._pretty_row(row)
            lines.append(line)
        return
