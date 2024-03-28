import sys
import os
import inspect
from datetime import datetime
from colorama import Fore, Style


# Thanks https://stackoverflow.com/a/9812105
def caller_name(skip=2):
    """Get a name of a caller in the format module.class.method

       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

       An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
      return ''
    parentframe = stack[start][0]    

    name = []
    module = inspect.getmodule(parentframe)
    if module:
        name.append(module.__name__)

    # detect classname
    if 'self' in parentframe.f_locals:
        name.append(parentframe.f_locals['self'].__class__.__name__)

    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append( codename ) # function or a method

    ## Avoid circular refs and frame leaks
    #  https://docs.python.org/2.7/library/inspect.html#the-interpreter-stack
    del parentframe, stack

    return ".".join(name)


class Log:
    @staticmethod
    def info(*argv) -> None:
        filename_full: str = inspect.stack()[1].filename
        filename: str = os.path.basename(filename_full)

        lineno: str = sys._getframe().f_back.f_lineno

        Log._impl_log("[INFO]", filename, lineno ,Fore.WHITE, *argv)

    @staticmethod
    def debug(*argv) -> None:
        filename_full: str = inspect.stack()[1].filename
        filename: str = os.path.basename(filename_full)

        lineno: str = sys._getframe().f_back.f_lineno

        Log._impl_log("[DEBUG]",  filename, lineno, Fore.MAGENTA, *argv)

    @staticmethod
    def warning(*argv) -> None:
        filename_full: str = inspect.stack()[1].filename
        filename: str = os.path.basename(filename_full)

        lineno: str = sys._getframe().f_back.f_lineno

        Log._impl_log("[WARN]",  filename, lineno, Fore.YELLOW, *argv)

    @staticmethod
    def error(*argv) -> None:
        filename_full: str = inspect.stack()[1].filename
        filename: str = os.path.basename(filename_full)

        lineno: str = sys._getframe().f_back.f_lineno

        Log._impl_log("[ERROR]",  filename, lineno, Fore.RED, *argv)

    @staticmethod
    def _impl_log(log_level: str, file: str, lineno: int, color: str, *argv) -> None:
        now: str = datetime.now().strftime('%H:%M:%S.%f')[:-3]

        caller = caller_name(3)

        print(f"{color}{log_level} " + Style.RESET_ALL, end='')
        print(f"{now} - {file} {caller}().{lineno} : ", end='')
        for arg in argv:
            print(f"{arg}", end='')

        print("")
