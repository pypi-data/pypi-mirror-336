"""
Provide custom exceptions.
"""

import buzz
from rich import traceback


# Enables prettified traceback printing via rich
traceback.install()


class DrivelError(buzz.Buzz):
    pass


class ThemeNotFound(DrivelError):
    pass


class ThemeReadError(DrivelError):
    pass


class ThemeWriteError(DrivelError):
    pass


class DuplicateTheme(DrivelError):
    pass
