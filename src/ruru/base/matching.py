"""Functionality for Argument Verification Using Partial Matching

This module provides Python equivalents of R's match.arg and pmatch functions.
Inspired by the R package `base` (https://stat.ethz.ch/R-manual/R-devel/library/base/html/00Index.html).
"""

from collections.abc import Iterable

from pydantic import validate_call


@validate_call
def match_arg(
    arg: str | list[str], choices: list[str], *, several_ok: bool = False
) -> str | list[str]:
    """Matches the argument(s) against a list of candidate values with partial matching.

    Provides Python equivalent of R's match.arg function with support for:
    - Exact string matching (preferred)
    - Partial string matching using prefix matching
    - Automatic deduplication of choices
    - Multiple matches when several_ok=True
    - Multi-string (list) input for batch matching
    - Proper error handling for ambiguous matches

    Inspired by: https://stat.ethz.ch/R-manual/R-devel/library/base/html/match.arg.html

    Args:
        arg: The argument string or list of strings to be matched against choices.
        choices: List of valid choices to match against. Duplicates are removed.
        several_ok: If True, allows multiple matches and always returns list.
                   If False, requires unique match. For list input, raises error.

    Returns:
        When arg is str and several_ok=False: Single matched string.
        When arg is str and several_ok=True: List containing matched string(s).
        When arg is list and several_ok=True: List containing all matched strings.
        For ambiguous matches with several_ok=True, returns all partial matches.

    Raises:
        ValueError: If no match found, if ambiguous match when several_ok=False,
                   or if list input provided when several_ok=False.
    """
    # Use pmatch for partial matching
    # Ensure choices are unique
    choices = list(dict.fromkeys(choices))

    # Handle list input
    if isinstance(arg, list):
        if not several_ok:
            error_message = (
                "List input is only allowed when several_ok=True. "
                "Use several_ok=True or provide a single string argument."
            )
            raise ValueError(error_message)

        # Process each element in the list
        all_matches = []
        for i, single_arg in enumerate(arg):
            try:
                # Recursively call match_arg for each element
                result = match_arg(single_arg, choices, several_ok=True)
                # result is always a list when several_ok=True
                all_matches.extend(result)
            except ValueError as e:
                # Re-raise with information about which element failed
                error_message = f"Error in list element {i} ('{single_arg}'): {e}"
                raise ValueError(error_message) from e

        return all_matches

    # Original single string logic below
    match_idx = pmatch(arg, choices)

    if match_idx is None:
        # No match found
        available_choices = ", ".join(choices)
        error_message = (
            f"The provided argument '{arg}' is not valid. "
            f"Available choices are: {available_choices}."
        )
        raise ValueError(error_message)
    elif match_idx == -1:
        # Ambiguous match
        if several_ok:
            # Return all partial matches when several_ok=True
            partial_matches = [choice for choice in choices if choice.startswith(arg)]
            return partial_matches
        else:
            # Error on ambiguous match when several_ok=False
            partial_matches = [choice for choice in choices if choice.startswith(arg)]
            matches_str = ", ".join(partial_matches)
            error_message = (
                f"The argument '{arg}' matches multiple choices: {matches_str}. "
                "Be more specific."
            )
            raise ValueError(error_message)
    else:
        # Unique match found
        matched_choice = choices[match_idx]
        if several_ok:
            return [matched_choice]
        return matched_choice


@validate_call
def pmatch(x: str, table: Iterable[str]) -> int | None:
    """Partial matching function similar to R's charmatch/pmatch.

    Performs partial string matching following R's behavior:
    - Prefer exact match (return 0-based index)
    - If unique prefix match, return index
    - If no match, return None
    - If ambiguous (multiple prefix matches), return -1
    - Empty string matches nothing

    Inspired by: https://stat.ethz.ch/R-manual/R-devel/library/base/html/pmatch.html

    Args:
        x: String to match
        table: Iterable of strings to match against

    Returns:
        Index of match if found and unique, -1 if ambiguous, None if no match
    """
    if not x:  # Empty string matches nothing
        return None

    table_list = list(table)

    # First check for exact match
    try:
        return table_list.index(x)
    except ValueError:
        pass

    # Check for prefix matches
    matches = [i for i, choice in enumerate(table_list) if choice.startswith(x)]

    if not matches:
        return None
    elif len(matches) == 1:
        return matches[0]
    else:
        return -1  # Ambiguous
