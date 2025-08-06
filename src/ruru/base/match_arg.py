"""Functionality for Argument Verification Using Partial Matching

Inspired by the R package `base` (https://www.rdocumentation.org/packages/base/versions/3.6.2/topics/match.arg).
"""


def match_arg(arg: str, choices: list[str]) -> str:
    """Matches the argument against a list of candidate values.

    Args:
        arg (str): The argument to be matched.
        choices (List[str]): A list of valid choices.

    Raises:
        ValueError: If the argument is not part of the choices.

    Returns:
        str: The matching choice.
    """
    error_msg = (
        f"The provided argument '{arg}' is not valid. "
        f"Available choices are: {', '.join(choices)}."
    )
    if arg not in choices:
        raise ValueError(error_msg)
    return arg
