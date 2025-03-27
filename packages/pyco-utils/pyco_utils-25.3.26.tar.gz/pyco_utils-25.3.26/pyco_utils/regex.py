import re


class RegexNotMatchError(Exception):
    def __init__(_self_, patten: str, value="", key="", note=""):
        ## {_self_, **kwargs} 
        _self_.kwargs = locals()
        _self_.msg = f"invalid ${key}({value}), unmatched patten<{patten}>({note})"
        _self_.errno = 40005
        print(_self_.errno, _self_.msg)


class PattenItem(object):
    def __init__(self, patten="", note="", key=None, zh=""):
        self.patten = patten
        self.note = note
        self.key = key
        self.zh = zh

    def to_dict(self):
        return vars(self)

    def match(self, value: str, silent=True, key=None):
        m = re.match(self.patten, value)
        if not m and not silent:
            vkey = key or self.key or self.zh or ''
            raise RegexNotMatchError(self.patten, value, vkey, self.note)
        return m


class PattenMeta(type):
    def __getattribute__(self, item):
        m = super().__getattribute__(item)
        if isinstance(m, PattenItem) and m.key is None:
            m.key = item
        return m


class RegexMap(metaclass=PattenMeta):
    ## usage:
    """
    RegexMap.datestr.match("1.2.4")
    #># <re.Match object; span=(0, 5), match='1.2.3'>
    RegexMap.datestr.match("v1.2.4", silent=False)
    #># Raise RegexNotMatchError
    """
    #  
    version = PattenItem(
        patten="\d+(?:\.\d+)*",
        note="由数字和小数点组成，eg: 1.2.4",
        zh="版本号",
    )

    datestr = PattenItem(
        patten="^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$",
        note="DateString:  yyyy-mm-dd 或 yyyy-m-d",
        zh="日期",
    )

    field_key = PattenItem(
        patten='^([a-zA-Z_]+)([a-zA-Z0-9_\.-]){2,63}$',
        note="首字符为字母, 长度不超过64，由字母数字组成的字符串（不允许空格, 符号仅支持_-.）",
        zh='索引键',
    )

    var_name = PattenItem(
        patten="^[A-Za-z_][A-Za-z0-9_]*$",
        note="首字符为字母, 仅由字母数字和下划线组成的字符串",
        zh='变量名',
    )

    var_type = PattenItem(
        patten="^<class '([a-zA-Z]+)'>$",
        note='输入值为type(value), eg: "<class \'int\'>"',
        zh='值类型',
    )

    def __getattribute__(self, item):
        m = super().__getattribute__(item)
        if isinstance(m, PattenItem) and m.key is None:
            m.key = item
        return m

    @classmethod
    def to_dict(cls):
        d = {}
        for k, m in vars(cls).items():
            if isinstance(m, PattenItem):
                d[k] = m.to_dict()
        return d


class RegexFilter():
    ignored_values = ["*", "", "None", "none", "undefined"]

    @classmethod
    def fuzzy_check(cls, target, condition: dict, strict=True, **kwargs):
        """
        @strict: True: AND: validate all kws of $condition
                 false: OR: 满足其中之一即可
        """
        ignored_values = kwargs.get("ignored_values", cls.ignored_values)
        if not condition:
            return True
        if isinstance(target, dict):
            _get = lambda k: target.get(k, None)
        else:
            _get = lambda k: getattr(target, k, None)
        for k, pt in condition.items():
            if pt in ignored_values:
                continue
            elif isinstance(pt, PattenItem):
                v2 = str(_get(k))
                pt2 = pt.patten
            else:
                pt2 = str(pt).strip()
                v2 = str(_get(k))
            if strict:
                if not bool(re.search(pt2, v2)):
                    return False
            else:
                if bool(re.search(pt2, v2)):
                    return True
        return strict


def alphanumeric(s: str, sep='_'):
    """
    # refer: https://stackoverflow.com/a/12985459/6705684
    # Note that \W is equivalent to [^a-zA-Z0-9_] only in Python 2.x.
    # In Python 3.x, \W+ is equivalent to [^a-zA-Z0-9_] only if re.ASCII / re.A flag is used.
    >>> alphanumeric('h^&ell`.,|o w]{+orld')
    'h_ell_o_w_orld'
    """
    return re.sub('[^0-9a-zA-Z]+', sep, s.strip())


def simple_case(s: str):
    """
    # better pathname/filename, accept only alpha numbers and [_-.]
    >>>simple_case("xxasdfIS _asdkf ks. asfx - dkasx"))
    'xxasdfIS_asdkfks.asfx-dkasx'
    >>>simple_case("xxasdfIS ÓÔÔLIasdf_asdkf中文ks. asfx - dkasx"))
    'xxasdfISLIasdf_asdkfks.asfx-dkasx'
    """
    return re.sub(r"[^0-9a-zA-Z_\-\.]+", '', s)


def snake_case(s: str):
    """
    # refer: https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    # smarter than ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')
    >>> snake_case('getHTTPResponseCode')
    'get_http_response_code'
    >>> snake_case('get2HTTPResponseCode')
    'get2_http_response_code'
    >>> snake_case('get2HTTPResponse123Code')
    'get2_http_response123_code'
    >>> snake_case('HTTPResponseCode')
    'http_response_code'
    >>> snake_case('HTTPResponseCodeXYZ')
    'http_response_code_xyz'
    """
    s = alphanumeric(s, '_')
    a = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
    return a.sub(r'_\1', s).lower()


def camel_case(s: str):
    """
    # suggest to preprocess $s with $simple_case or $alphanumeric
    >>> camel_case("Some rise ^升起^. Some fade ª••º.")
    'SomeRise ^升起^. SomeFade ª••º.'
    >>> camel_case("Some live to die another day.")
    'SomeLiveToDieAnotherDay.'
    >>> camel_case("I’ll live to die another day.")
    'I’llLiveToDieAnotherDay.'
    """
    return re.sub(r"[\-_\.\s]([a-z])", lambda mo: mo.group(1).upper(), s)


def title_case(s: str):
    """
    # refer: https://docs.python.org/3/library/stdtypes.html#str.title
    >>> title_case("they're bill's friends.")
    "They're Bill's Friends."
    """
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0).capitalize(), s)
