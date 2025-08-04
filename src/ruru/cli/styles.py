"""Text styling and color utilities.

Contains functions for bold, dim, italic, underline, and color formatting.
"""


class BColours:
    """A class providing ANSI escape codes for color formatting.

    This class provides ANSI escape codes for color formatting. It is used by
    the CLI class to print colored messages.
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def blue(text: str) -> str:
    """Color the text blue."""
    return f"{BColours.BOLD}{BColours.OKBLUE}{text}{BColours.ENDC}"


def cyan(text: str) -> str:
    """Color the text cyan."""
    return f"{BColours.BOLD}{BColours.OKCYAN}{text}{BColours.ENDC}"


def green(text: str) -> str:
    """Color the text green."""
    return f"{BColours.BOLD}{BColours.OKGREEN}{text}{BColours.ENDC}"


def orange(text: str) -> str:
    """Color the text orange."""
    return f"{BColours.BOLD}{BColours.WARNING}{text}{BColours.ENDC}"
