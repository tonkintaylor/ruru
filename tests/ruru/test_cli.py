import pytest

from ruru.cli import CLI


@pytest.mark.parametrize(
    ("method", "args", "expects_print"),
    [
        (CLI.h1, ("Test Heading 1",), True),
        (CLI.h2, ("Test Heading 2",), True),
        (CLI.h3, ("Test Heading 3",), True),
        (CLI.alert_success, ("Success message",), True),
        (CLI.alert_danger, ("Danger message",), True),
        (CLI.alert_warning, ("Warning message",), True),
        (CLI.alert_info, ("Info message",), True),
        (CLI.bullets, (["Item 1", "Item 2"],), True),
        (CLI.blue, ("Blue text",), False),
        (CLI.cyan, ("Cyan text",), False),
        (CLI.green, ("Green text",), False),
        (CLI.orange, ("Orange text",), False),
    ],
)
def test_cli_methods_output(
    capfd: pytest.CaptureFixture[str], method, args, expects_print
):
    """Test the output of a CLI method.

    Args:
        capfd (pytest fixture): Captures the stdout and stderr output.
        method (function): The CLI method to test.
        args (tuple): The arguments to pass to the method.
        expects_print (bool): Indicates whether the method is expected to print.

    Returns:
        None

    Raises:
        AssertionError: If the method does not produce the expected output.
    """
    result = method(*args)
    if expects_print:
        out = capfd.readouterr()
        assert out, "Expected method to print something, but it didn't."
    else:
        assert result != args[0], (
            "Expected method to return a colored string, but it didn't."
        )


@pytest.mark.parametrize(
    ("method", "args"),
    [
        (CLI.blue, ("Blue text",)),
        (CLI.cyan, ("Cyan text",)),
        (CLI.green, ("Green text",)),
        (CLI.orange, ("Orange text",)),
    ],
)
def test_cli_color_methods_return_values(method, args):
    """Test the return values of color methods.

    This function calls the specified `method` with the given `args` and checks if the result is a colored string.
    If the result is not a colored string, an assertion error is raised.

    Args:
        method: The color method to test.
        args: The arguments to pass to the color method.

    Raises:
        AssertionError: If the method does not return a colored string.

    Returns:
        None
    """  # noqa: E501
    result = method(*args)
    assert result != args[0], (
        "Expected method to return a colored string, but it didn't."
    )
