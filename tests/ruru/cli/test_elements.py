import pytest

from ruru import cli


@pytest.mark.parametrize("heading_func", [cli.h1, cli.h2, cli.h3])
def test_heading_functions_produce_output(capfd, heading_func):
    """Test heading functions produce output."""
    heading_func("Test Heading")
    captured = capfd.readouterr()
    assert captured.out != ""


@pytest.mark.parametrize(
    ("alert_func", "msg"),
    [
        (cli.alert_success, "Success!"),
        (cli.alert_danger, "Danger!"),
        (cli.alert_warning, "Warning!"),
        (cli.alert_info, "Info!"),
        (cli.alert_note, "Note!"),
    ],
)
def test_alert_functions_produce_output(capfd, alert_func, msg):
    """Test alert functions produce output."""
    alert_func(msg)
    captured = capfd.readouterr()
    assert captured.out != ""


@pytest.mark.parametrize("items", [["Item 1", "Item 2", "Item 3"]])
def test_bullets_produce_output(capfd, items):
    """Test bullets function produces output."""
    cli.bullets(items)
    captured = capfd.readouterr()
    assert captured.out != ""
