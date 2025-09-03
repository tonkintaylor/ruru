"""Semantic building blocks for CLI output.

Contains functions for headings, alerts, paragraphs, rules, lists, boxes, trees,
and print helpers.
"""

from os import get_terminal_size
from typing import Any

from ruru.cli.styles import blue, bold, green, red, yellow
from ruru.cli.symbols import bullet, cross, info, line, tick, warning


def h1(text: str) -> None:
    """Prints a level 1 heading.

    Args:
        text: The text to be displayed as a heading.

    Examples:
        >>> h1("hello")
        ──────────────────────── hello ────────────────────────
    """
    try:
        columns = get_terminal_size().columns
    except OSError:
        columns = 80
    line_length = columns
    dashes = line() * ((line_length - len(text)) // 2 - 1)
    print(f"\n{dashes} {text} {dashes}\n")


def h2(text: str) -> None:
    """Prints a level 2 heading.

    Args:
        text: The text to be displayed as a heading.

    Examples:
        >>> h2("hello world")
        ── hello world ──
    """
    print(f"\n── {text} ──\n")


def h3(text: str) -> None:
    """Prints a level 3 heading.

    Args:
        text: The text to be displayed as a heading.

    Examples:
        >>> h3("hello")
        ── hello
    """
    print(f"\n── {text}\n")


def alert_success(message: str) -> None:
    """Prints a success message in green color.

    Args:
        message: The message to be displayed.

    Examples:
        >>> alert_success("This is a success message.")
        ✔ This is a success message.
    """
    print(bold(green(tick())), message)


def alert_danger(message: str) -> None:
    """Prints a danger message in red color.

    Args:
        message: The message to be displayed.

    Examples:
        >>> alert_danger("Danger! Something went wrong.")
        ✖ Danger! Something went wrong.
    """
    print(bold(red(cross())), message)


def alert_warning(message: str) -> None:
    """Prints a warning message in yellow color.

    Args:
        message: The message to be displayed.

    Examples:
        >>> alert_warning("Warning: Proceed with caution.")
        ! Warning: Proceed with caution.
    """
    print(bold(yellow(warning())), message)


def alert_info(message: str) -> None:
    """Prints an information message in blue color.

    Args:
        message: The message to be displayed.

    Examples:
        >>> alert_info("Information: This is important.")
        ℹ Information: This is important.
    """
    print(bold(blue(info())), message)


def alert_note(message: str) -> None:
    """Prints a note message in a default color.

    Args:
        message: The message to be displayed.

    Examples:
        >>> alert_note("This is a note.")
        ℹ This is a note.
    """
    print(bold(info()), message)


def bullets(text: list[Any] | dict[str, Any]) -> None:
    """Prints a list of items or dict key-value pairs with bullet points.

    Args:
        text: A list of items (strings, numbers, etc.) to be displayed with bullet points, 
            or a dict of key-value pairs to be displayed as "• key: value".

    Examples:
        >>> bullet_list = ["Item 1", "Item 2", "Item 3"]
        >>> bullets(bullet_list)
        • Item 1
        • Item 2
        • Item 3

        >>> mixed_list = ["Text item", 42, 3.14]
        >>> bullets(mixed_list)
        • Text item
        • 42
        • 3.14

        >>> bullet_dict = {"name": "John", "age": 30, "hobbies": ["reading", "coding"]}
        >>> bullets(bullet_dict)
        • name: John
        • age: 30
        • hobbies: reading, coding
    """
    if isinstance(text, dict):
        for key, value in text.items():
            if isinstance(value, list):
                formatted_value = ", ".join(str(v) for v in value)
            else:
                formatted_value = str(value)
            print(f"  {bullet()}", f"{key}: {formatted_value}")
    else:
        for item in text:
            print(f"  {bullet()}", str(item))
