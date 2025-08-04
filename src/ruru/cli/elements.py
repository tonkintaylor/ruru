"""Semantic building blocks for CLI output.

Contains functions for headings, alerts, paragraphs, rules, lists, boxes, trees,
and print helpers.
"""

from os import get_terminal_size


def h1(text: str) -> None:  # pylint: disable=invalid-name
    """Prints a level 1 heading.

    Args:
        text: The text to be displayed as a heading.

    Examples:
        >>> h1("hello")  # doctest: +SKIP
        ──────────────────────── hello ────────────────────────
    """
    try:
        columns = get_terminal_size().columns
    except OSError:
        columns = 80
    line_length = columns
    dashes = "─" * ((line_length - len(text)) // 2 - 1)
    print(f"\n{dashes} {text} {dashes}\n")


def h2(text: str) -> None:  # pylint: disable=invalid-name
    """Prints a level 2 heading.

    Args:
        text: The text to be displayed as a heading.

    Examples:
        >>> h2("hello world")  # doctest: +SKIP
        ── hello world ──
    """
    print(f"\n── {text} ──\n")


def h3(text: str) -> None:  # pylint: disable=invalid-name
    """Prints a level 3 heading.

    Args:
        text: The text to be displayed as a heading.

    Examples:
        >>> h3("hello")  # doctest: +SKIP
        ── hello
    """
    print(f"\n── {text}\n")


def alert_success(message: str) -> None:
    """Prints a success message in green color.

    Args:
        message: The message to be displayed.

    Examples:
        >>> alert_success("This is a success message.")  # doctest: +SKIP
        ✔ This is a success message.
    """
    print("\033[1m\033[32m✔\033[0m", message)


def alert_danger(message: str) -> None:
    """Prints a danger message in red color.

    Args:
        message: The message to be displayed.

    Examples:
        >>> alert_danger("Danger! Something went wrong.")  # doctest: +SKIP
        ✖ Danger! Something went wrong.
    """
    print("\033[1m\033[31m✖\033[0m", message)


def alert_warning(message: str) -> None:
    """Prints a warning message in yellow color.

    Args:
        message: The message to be displayed.

    Examples:
        >>> alert_warning("Warning: Proceed with caution.")  # doctest: +SKIP
        ! Warning: Proceed with caution.
    """
    print("\033[1m\033[33m!\033[0m", message)


def alert_info(message: str) -> None:
    """Prints an information message in blue color.

    Args:
        message: The message to be displayed.

    Examples:
        >>> alert_info("Information: This is important.")  # doctest: +SKIP
        ℹ Information: This is important.
    """
    print("\033[1m\033[34mℹ\033[0m", message)


def alert_note(message: str) -> None:
    """Prints a note message in a default color.

    Args:
        message: The message to be displayed.

    Examples:
        >>> alert_note("This is a note.")  # doctest: +SKIP
        ℹ This is a note.
    """
    print("\033[1mℹ\033[0m", message)


def bullets(text: list[str]) -> None:
    """Prints a list of items with bullet points.

    Args:
        text: A list of items to be displayed with bullet points.

    Examples:
        >>> bullet_list = ["Item 1", "Item 2", "Item 3"]
        >>> bullets(bullet_list)  # doctest: +SKIP
        • Item 1
        • Item 2
        • Item 3
    """
    for item in text:
        print("  •", item)
