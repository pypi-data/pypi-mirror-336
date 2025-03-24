import os
import math
import sys
import signal


# TODO: check if process already exists and exit if so
class Process:
    pid: int

    def __init__(self, pid=None):
        self.pid = pid if pid is not None else os.getpid()

        try:
            process_uid = os.stat(f"/proc/{self.pid}").st_uid
        except FileNotFoundError:
            msg = f"Process with PID {self.pid} doesn't exist"
            raise ProcessLookupError(msg)

        if process_uid != os.getuid():
            msg = "You don't have permissions to control this process"
            raise PermissionError(msg)

    def terminate(self):
        os.kill(self.pid, signal.SIGTERM)

    def kill(self):
        os.kill(self.pid, signal.SIGKILL)

    def send_signal(self, sig: int | str):
        if isinstance(sig, str):
            sig_num = getattr(signal, sig)
        elif isinstance(sig, int):
            sig_num = sig
        else:
            raise TypeError("Invalid type for signal")

        os.kill(self.pid, sig_num)

    def _is_dwm_status_bar(self, pid: int) -> bool:
        try:
            with open(f"/proc/{pid}/cmdline") as file:
                argv = file.read().split("\0")

            argv0 = os.path.basename(argv[0])
            if not argv0 in ["python", "python3",
                             os.path.basename(sys.executable)]:
                return False

            index = self._get_name_index_from_argv(argv)
            if index == -1:
                return False

            return True

        except FileNotFoundError:
            return False

    def _get_name_index_from_argv(self, argv: list[str]):
        if not isinstance(argv, list):
            raise TypeError("argv must be a list[str]")
        for arg in argv:
            if not isinstance(arg, str):
                raise TypeError("argv must be a list[str]")

        index = -1
        args = list(map(lambda f: os.path.basename(f), argv))
        try:
            index = args.index("dwm-status-bar")
            return index
        except ValueError:
            pass

        index = argv.index("-m") + 1
        if argv[index] != "dwm_status_bar":
            return -1

        return index


def trait(*methods, **named_methods):
    """
    A decorator to be used with class definitions. Dynamically add any
    functions passed as arguments to a class as methods. You can also
    choose method names by passing them as keyword arguments.
    """
    def implement(cls):
        for method in methods:
            name = method.__name__
            setattr(cls, name, method)

        for name, method in named_methods.items():
            method.__name__ = name
            setattr(cls, name, method)

        return cls
    return implement


def number_size(num):
    """
    Return how many characters are necessary to write a number. This
    function should only be used for numbers ranging from 0 to 100.
    """
    if num == 0:
        return 1
    log10 = math.log(abs(num), 10)
    result = math.floor(log10) + 1
    return result


def format_number(num, width, precision):
    """
    Format a number with a given width and precision. If the resulting
    string representation is too large, the precision is reduced so the
    number can fit within the chosen width.
    """
    size = number_size(num)
    if size + precision + 1 > width:
        precision = max(width - size - 1, 0)
    return f"{num:>{width}.{precision}f}"


def create_pid_file(pid: int) -> str:
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
    if runtime_dir is not None:
        filename = os.path.join(runtime_dir, "dwm_status_bar.pid")
    else:
        dirname = f"/tmp/dwm_status_bar_{os.getuid()}"
        filename = os.path.join(dirname, "dwm_status_bar.pid")
        os.makedirs(dirname, mode=0o700, exist_ok=True)

    with open(filename, "x") as pid_file:
        pid_file.write(str(pid))
        pid_file.write("\n")

    return filename


def find_process():
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
    if runtime_dir is not None:
        filename = os.path.join(runtime_dir, "dwm_status_bar.pid")
    else:
        dirname = f"/tmp/dwm_status_bar_{os.getuid()}"
        filename = os.path.join(dirname, "dwm_status_bar.pid")

    try:
        with open(filename, "r") as pid_file:
            pid = pid_file.read()
        return Process(int(pid))
    except FileNotFoundError:
        return None
