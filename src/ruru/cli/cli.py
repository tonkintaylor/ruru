from ruru.cli.elements import (
    alert_danger,
    alert_info,
    alert_note,
    alert_success,
    alert_warning,
    bullets,
    h1,
    h2,
    h3,
)


class CLI:
    """A class providing CLI alert functions for displaying colored messages.

    This class provides functions to print alert messages in different colors
    and styles. It uses ANSI escape codes for color formatting.

    Reference: https://cli.r-lib.org/reference/index.html
    """

    @staticmethod
    def h1(text: str) -> None:  # pylint: disable=invalid-name
        """Prints a level 1 heading.

        Args:
            text: The text to be displayed as a heading.

        Examples:
            >>> CLI.h1("hello")
            ──────────────────────── hello ────────────────────────
        """
        h1(text)

    @staticmethod
    def h2(text: str) -> None:  # pylint: disable=invalid-name
        """Prints a level 2 heading.

        Args:
            text: The text to be displayed as a heading.

        Examples:
            >>> CLI.h2("hello world")
            ── hello world ──
        """
        h2(text)

    @staticmethod
    def h3(text: str) -> None:  # pylint: disable=invalid-name
        """Prints a level 3 heading.

        Args:
            text: The text to be displayed as a heading.

        Examples:
            >>> CLI.h3("hello")
            ── hello
        """
        h3(text)

    @staticmethod
    def alert_success(message: str) -> None:
        """Prints a success message in green color.

        Args:
            message: The message to be displayed.

        Examples:
            >>> CLI.alert_success("This is a success message.")
            ✔ This is a success message.
        """
        alert_success(message)

    @staticmethod
    def alert_danger(message: str) -> None:
        """Prints a danger message in red color.

        Args:
            message: The message to be displayed.

        Examples:
            >>> CLI.alert_danger("Danger! Something went wrong.")
            ✖ Danger! Something went wrong.
        """
        alert_danger(message)

    @staticmethod
    def alert_warning(message: str) -> None:
        """Prints a warning message in yellow color.

        Args:
            message: The message to be displayed.

        Examples:
            >>> CLI.alert_warning("Warning: Proceed with caution.")
            ! Warning: Proceed with caution.
        """
        alert_warning(message)

    @staticmethod
    def alert_info(message: str) -> None:
        """Prints an information message in blue color.

        Args:
            message: The message to be displayed.

        Examples:
            >>> CLI.alert_info("Information: This is important.")
            ℹ Information: This is important.
        """
        alert_info(message)

    @staticmethod
    def alert_note(message: str) -> None:
        """Prints a note message in a default color.

        Args:
            message: The message to be displayed.

        Examples:
            >>> CLI.alert_note("This is a note.")
            ℹ This is a note.
        """
        alert_note(message)

    @staticmethod
    def bullets(text: list[str]) -> None:
        """Prints a list of items with bullet points.

        Args:
            text: A list of items to be displayed with bullet points.

        Examples:
            >>> bullet_list = ["Item 1", "Item 2", "Item 3"]
            >>> CLI.bullets(bullet_list)
            • Item 1
            • Item 2
            • Item 3
        """
        bullets(text)
