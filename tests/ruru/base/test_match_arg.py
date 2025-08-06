import pytest

from ruru.base.match_arg import match_arg


class TestMatchArg:
    """Tests for the match_arg function."""

    def test_valid_arg(self):
        """Test match_arg with a valid argument."""
        choices = ["apple", "banana", "cherry"]
        result = match_arg("banana", choices)
        assert result == "banana", "The function should return the matched argument."

    def test_invalid_arg(self):
        """Test match_arg with an invalid argument."""
        choices = ["apple", "banana", "cherry"]
        error_msg = (
            "The provided argument 'orange' is not valid. "
            "Available choices are: apple, banana, cherry."
        )
        with pytest.raises(ValueError, match=error_msg):
            match_arg("orange", choices)
