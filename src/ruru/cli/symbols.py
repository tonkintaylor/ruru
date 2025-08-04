"""Unicode symbols with ASCII alternatives for CLI output."""

import os
import sys
from typing import Literal


def _supports_unicode() -> bool:
    """Check if the terminal supports Unicode characters."""
    # Check if ASCII_ONLY environment variable is set
    if os.getenv("ASCII_ONLY"):
        return False

    # Check encoding
    encoding = getattr(sys.stdout, "encoding", "").lower()
    return encoding in ("utf-8", "utf8")


SymbolName = Literal[
    "tick",
    "cross",
    "warning",
    "info",
    "arrow_right",
    "bullet",
    "line",
    "corner",
    "tree_mid",
    "tree_end",
]


# Symbol definitions with Unicode and ASCII alternatives
_SYMBOLS = {
    "tick": {"unicode": "✔", "ascii": "v"},
    "cross": {"unicode": "✖", "ascii": "x"},
    "warning": {"unicode": "⚠", "ascii": "!"},
    "info": {"unicode": "ℹ", "ascii": "i"},
    "arrow_right": {"unicode": "→", "ascii": "->"},
    "bullet": {"unicode": "•", "ascii": "*"},
    "line": {"unicode": "─", "ascii": "-"},
    "corner": {"unicode": "└", "ascii": "+"},
    "tree_mid": {"unicode": "├", "ascii": "+"},
    "tree_end": {"unicode": "└", "ascii": "+"},
}


def symbol(name: SymbolName) -> str:
    """Get a symbol with Unicode or ASCII alternative based on terminal support.

    Args:
        name: Name of the symbol to retrieve.

    Returns:
        Unicode symbol if supported, otherwise ASCII alternative.

    Raises:
        ValueError: If symbol name is not recognized.
    """
    if name not in _SYMBOLS:
        msg = f"Unknown symbol: {name}"
        raise ValueError(msg)

    symbol_def = _SYMBOLS[name]

    if _supports_unicode():
        return symbol_def["unicode"]
    return symbol_def["ascii"]


# Convenience functions for common symbols
def tick() -> str:
    """Get tick/checkmark symbol."""
    return symbol("tick")


def cross() -> str:
    """Get cross/X symbol."""
    return symbol("cross")


def warning() -> str:
    """Get warning symbol."""
    return symbol("warning")


def info() -> str:
    """Get info symbol."""
    return symbol("info")


def arrow_right() -> str:
    """Get right arrow symbol."""
    return symbol("arrow_right")


def bullet() -> str:
    """Get bullet point symbol."""
    return symbol("bullet")


def line() -> str:
    """Get horizontal line symbol."""
    return symbol("line")


def corner() -> str:
    """Get corner symbol for boxes/trees."""
    return symbol("corner")


def tree_mid() -> str:
    """Get tree middle connector symbol."""
    return symbol("tree_mid")


def tree_end() -> str:
    """Get tree end connector symbol."""
    return symbol("tree_end")
