import sys


_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)


try:
    from builtins import FileNotFoundError
except ImportError:
    class FileNotFoundError(OSError):
        pass


if is_py2:
    basestring = basestring
    numeric_types = (int, long, float)
    integer_types = (int, long)
elif is_py3:
    basestring = (str, bytes)
    numeric_types = (int, float)
    integer_types = (int,)
