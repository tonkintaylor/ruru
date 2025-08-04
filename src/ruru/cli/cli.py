from os import get_terminal_size


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
        try:
            columns = get_terminal_size().columns
        except OSError:
            columns = 80
        line_length = columns
        dashes = "─" * ((line_length - len(text)) // 2 - 1)
        print(f"\n{dashes} {text} {dashes}\n")

    @staticmethod
    def h2(text: str) -> None:  # pylint: disable=invalid-name
        """Prints a level 2 heading.

        Args:
            text: The text to be displayed as a heading.

        Examples:
            >>> CLI.h2("hello world")
            ── hello world ──
        """
        print(f"\n── {text} ──\n")

    @staticmethod
    def h3(text: str) -> None:  # pylint: disable=invalid-name
        """Prints a level 3 heading.

        Args:
            text: The text to be displayed as a heading.

        Examples:
            >>> CLI.h3("hello")
            ── hello
        """
        print(f"\n── {text}\n")

    @staticmethod
    def alert_success(message: str) -> None:
        """Prints a success message in green color.

        Args:
            message: The message to be displayed.

        Examples:
            >>> CLI.alert_success("This is a success message.")
            ✔ This is a success message.
        """
        print("\033[1m\033[32m✔\033[0m", message)

    @staticmethod
    def alert_danger(message: str) -> None:
        """Prints a danger message in red color.

        Args:
            message: The message to be displayed.

        Examples:
            >>> CLI.alert_danger("Danger! Something went wrong.")
            ✖ Danger! Something went wrong.
        """
        print("\033[1m\033[31m✖\033[0m", message)

    @staticmethod
    def alert_warning(message: str) -> None:
        """Prints a warning message in yellow color.

        Args:
            message: The message to be displayed.

        Examples:
            >>> CLI.alert_warning("Warning: Proceed with caution.")
            ! Warning: Proceed with caution.
        """
        print("\033[1m\033[33m!\033[0m", message)

    @staticmethod
    def alert_info(message: str) -> None:
        """Prints an information message in blue color.

        Args:
            message: The message to be displayed.

        Examples:
            >>> CLI.alert_info("Information: This is important.")
            ℹ Information: This is important.
        """
        print("\033[1m\033[34mℹ\033[0m", message)

    @staticmethod
    def alert_note(message: str) -> None:
        """Prints a note message in a default color.

        Args:
            message: The message to be displayed.

        Examples:
            >>> CLI.alert_note("This is a note.")
            ℹ This is a note.
        """
        print("\033[1mℹ\033[0m", message)

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
        for item in text:
            print("  •", item)

    @staticmethod
    def blue(text: str) -> str:
        """Color the text blue."""
        return f"{BColours.BOLD}{BColours.OKBLUE}{text}{BColours.ENDC}"

    @staticmethod
    def cyan(text: str) -> str:
        """Color the text cyan."""
        return f"{BColours.BOLD}{BColours.OKCYAN}{text}{BColours.ENDC}"

    @staticmethod
    def green(text: str) -> str:
        """Color the text green."""
        return f"{BColours.BOLD}{BColours.OKGREEN}{text}{BColours.ENDC}"

    @staticmethod
    def orange(text: str) -> str:
        """Color the text orange."""
        return f"{BColours.BOLD}{BColours.WARNING}{text}{BColours.ENDC}"


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
