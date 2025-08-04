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
    ],
)
def test_cli_methods_output(
    capfd: pytest.CaptureFixture[str], method, args, expects_print
):
    """Test CLI method output."""
    result = method(*args)
    if expects_print:
        out = capfd.readouterr()
        assert out, "Expected method to print something, but it didn't."
    else:
        assert result != args[0], (
            "Expected method to return a colored string, but it didn't."
        )
