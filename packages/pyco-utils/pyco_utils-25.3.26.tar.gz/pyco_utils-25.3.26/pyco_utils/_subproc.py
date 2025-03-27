import subprocess


class PycoTaskStatusTP():
    code = 0
    msg = "执行成功"

    def __init__(self, code=0, msg="", data=None):
        self.code = code
        self.msg = msg
        self.data = data

    def __str__(self):
        return f"{self.code}:{self.msg}"

    def __bool__(self):
        ### 任务成功: returncode == 0 
        return self.code == 0

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.code == other.code
        if isinstance(other, int):
            return self.code == other
        if isinstance(other, str):
            alias = [str(self.code), self.msg, f"{self.code}:{self.msg}"]
            return other in alias
        return id(other) == id(self.data)


    def __call__(self, data):
        if isinstance(data, self.__class__):
            return data
        m = self.__class__(self.code, self.msg)
        m.data = data
        return m

    def to_json(self):
        m = dict(
            code=self.code,
            msg=self.msg,
        )
        if self.data is not None:
            m["data"] = self.data
        return m


def run_subpopen(command, **kwargs):
    stdout = kwargs.pop("stdout", subprocess.PIPE)
    stderr = kwargs.pop("stderr", subprocess.PIPE)
    # cmd = subprocess.run(command, shell=shell, capture_output=True)
    cmd = subprocess.Popen(command, stdout=stdout, stderr=stderr, **kwargs)
    cmd.wait()
    return cmd


def run_subprocess(command, **kwargs):
    """
    subprocess.run was added in Python 3.5 as a simplification over subprocess.
    Popen when you just want to execute a command and wait until it finishes,
     but you don't want to do anything else meanwhile.
      For other cases, you still need to use subprocess.Popen.
    """
    try:
        print(f"[TODO] {command} ")
        cmd = subprocess.run(command, **kwargs)
        msg = (f"[OK] {command} ") 
        if not cmd.returncode == 0:
            msg = f"[Fail] {command} "
        print(msg)
        return PycoTaskStatusTP(cmd.returncode, msg, kwargs)
    except Exception as e:
        msg = f"[Error!!!] {command} \n {e} \n"
        print(msg)
        return PycoTaskStatusTP(-1, msg, kwargs)


def exec_command(command, shell=True, timeout_ss=None, **kwargs):
    # stdout = kwargs.pop("stdout", subprocess.PIPE)
    cmd = subprocess.Popen(command, shell=shell, **kwargs)
    cmd.wait(timeout_ss)
    result = cmd.stdout
    try:
        result = result.read()
    except Exception as e:
        print("[stdout]", result, e)
    if cmd.returncode == 0:
        return True, result, ""
    else:
        error = cmd.stderr
        try:
            error = error.read()
        except Exception as e:
            print("[stderr]", error, e)
        return False, result, error
