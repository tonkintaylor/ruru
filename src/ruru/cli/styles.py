"""ANSI color and text styling utilities for CLI output."""

import os
import sys
from typing import Literal


# ANSI escape codes for text styling
class _AnsiCodes:
    """ANSI escape codes for text formatting."""

    # Reset
    RESET = "\033[0m"

    # Text styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Colors (for the foreground)
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors (for the foreground)
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


def _supports_color() -> bool:
    """Check if the terminal supports ANSI color codes."""
    # Check if NO_COLOR environment variable is set
    if os.getenv("NO_COLOR"):
        return False

    # Check if FORCE_COLOR is set
    if os.getenv("FORCE_COLOR"):
        return True

    # For testing environments, always enable colors
    if "pytest" in sys.modules:
        return True

    # Check if output is a TTY
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False

    # Check TERM environment variable
    term = os.getenv("TERM", "").lower()
    return "color" in term or term in ("xterm", "xterm-256color", "screen", "linux")


def _apply_style(text: str, code: str) -> str:
    """Apply ANSI style code to text if color is supported."""
    if not _supports_color():
        return text
    return f"{code}{text}{_AnsiCodes.RESET}"


# Text style functions
def bold(text: str) -> str:
    """Make text bold."""
    return _apply_style(text, _AnsiCodes.BOLD)


def dim(text: str) -> str:
    """Make text dim/faint."""
    return _apply_style(text, _AnsiCodes.DIM)


def italic(text: str) -> str:
    """Make text italic."""
    return _apply_style(text, _AnsiCodes.ITALIC)


def underline(text: str) -> str:
    """Make text underlined."""
    return _apply_style(text, _AnsiCodes.UNDERLINE)


# Color functions
ColorName = Literal[
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "bright_black",
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_white",
]


def color(text: str, color_name: ColorName) -> str:
    """Apply a color to text."""
    color_map = {
        "black": _AnsiCodes.BLACK,
        "red": _AnsiCodes.RED,
        "green": _AnsiCodes.GREEN,
        "yellow": _AnsiCodes.YELLOW,
        "blue": _AnsiCodes.BLUE,
        "magenta": _AnsiCodes.MAGENTA,
        "cyan": _AnsiCodes.CYAN,
        "white": _AnsiCodes.WHITE,
        "bright_black": _AnsiCodes.BRIGHT_BLACK,
        "bright_red": _AnsiCodes.BRIGHT_RED,
        "bright_green": _AnsiCodes.BRIGHT_GREEN,
        "bright_yellow": _AnsiCodes.BRIGHT_YELLOW,
        "bright_blue": _AnsiCodes.BRIGHT_BLUE,
        "bright_magenta": _AnsiCodes.BRIGHT_MAGENTA,
        "bright_cyan": _AnsiCodes.BRIGHT_CYAN,
        "bright_white": _AnsiCodes.BRIGHT_WHITE,
    }

    if color_name not in color_map:
        msg = f"Unknown color: {color_name}"
        raise ValueError(msg)

    return _apply_style(text, color_map[color_name])


# Convenience color functions
def red(text: str) -> str:
    """Make text red."""
    return color(text, "red")


def green(text: str) -> str:
    """Make text green."""
    return color(text, "green")


def yellow(text: str) -> str:
    """Make text yellow."""
    return color(text, "yellow")


def blue(text: str) -> str:
    """Make text blue."""
    return color(text, "blue")


def magenta(text: str) -> str:
    """Make text magenta."""
    return color(text, "magenta")


def cyan(text: str) -> str:
    """Make text cyan."""
    return color(text, "cyan")


def orange(text: str) -> str:
    """Make text orange (alias for yellow)."""
    return color(text, "yellow")


# Backward compatibility alias
class BColours:
    """Backward compatibility class for legacy ANSI codes.

    This class is maintained for backward compatibility.
    New code should use the individual color functions instead.
    """

    HEADER = _AnsiCodes.BRIGHT_MAGENTA
    OKBLUE = _AnsiCodes.BRIGHT_BLUE
    OKCYAN = _AnsiCodes.BRIGHT_CYAN
    OKGREEN = _AnsiCodes.BRIGHT_GREEN
    WARNING = _AnsiCodes.BRIGHT_YELLOW
    FAIL = _AnsiCodes.BRIGHT_RED
    ENDC = _AnsiCodes.RESET
    BOLD = _AnsiCodes.BOLD
    UNDERLINE = _AnsiCodes.UNDERLINE
