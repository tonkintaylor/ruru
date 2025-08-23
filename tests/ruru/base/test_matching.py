"""Tests for the matching module functions."""

import pytest

from ruru.base.matching import match_arg, pmatch


@pytest.fixture
def standard_choices():
    """Standard test choices fixture."""
    return ["apple", "banana", "cherry"]


@pytest.fixture
def partial_match_choices():
    """Choices for partial matching tests."""
    return ["apple", "apricot", "banana"]


@pytest.fixture
def ambiguous_choices():
    """Choices that create ambiguous matches."""
    return ["mean", "median", "mode"]


@pytest.fixture
def integration_test_data():
    """Data for integration tests."""
    return {
        "exact_precedence": ["test", "testing", "tester"],
        "duplicate_exact": ["test", "other", "test"],
        "complex_partial": ["configure", "config", "confirm", "console"],
    }


class TestPmatch:
    """Tests for the pmatch helper function."""

    @pytest.mark.parametrize(
        ("query", "expected"),
        [
            ("median", 1),  # exact match returns correct index
            ("med", 1),  # unique prefix match returns index
            ("m", -1),  # ambiguous prefix returns -1
            ("xyz", None),  # no match returns None
            ("", None),  # empty string returns None
        ],
    )
    def test_pmatch_scenarios(self, ambiguous_choices, query, expected):
        """Test various pmatch scenarios."""
        result = pmatch(query, ambiguous_choices)
        assert result == expected


class TestMatchArgExactMatches:
    """Tests for exact matching functionality."""

    @pytest.mark.parametrize(
        ("several_ok", "expected"),
        [
            (False, "banana"),  # several_ok=False returns string
            (True, ["banana"]),  # several_ok=True returns list
        ],
    )
    def test_exact_match_behavior(self, standard_choices, several_ok, expected):
        """Test exact match behavior with different several_ok values."""
        result = match_arg("banana", standard_choices, several_ok=several_ok)
        assert result == expected

    def test_exact_match_default(self, standard_choices):
        """Test exact match with default parameters."""
        result = match_arg("banana", standard_choices)
        assert result == "banana"


class TestMatchArgPartialMatches:
    """Tests for partial matching functionality."""

    @pytest.mark.parametrize(
        ("several_ok", "expected"),
        [
            (False, "banana"),  # several_ok=False returns string
            (True, ["banana"]),  # several_ok=True returns list
        ],
    )
    def test_partial_match_unique(self, partial_match_choices, several_ok, expected):
        """Test unique partial match with different several_ok values."""
        result = match_arg("ban", partial_match_choices, several_ok=several_ok)
        assert result == expected


class TestMatchArgAmbiguousMatches:
    """Tests for ambiguous match handling."""

    def test_ambiguous_match_error(self, partial_match_choices):
        """Test that ambiguous partial match raises error when several_ok=False."""
        with pytest.raises(ValueError, match="matches multiple choices"):
            match_arg("ap", partial_match_choices)

    @pytest.mark.parametrize(
        ("query", "choices", "expected"),
        [
            ("ap", ["apple", "apricot", "banana"], ["apple", "apricot"]),
            ("a", ["zebra", "apple", "apricot", "ant"], ["apple", "apricot", "ant"]),
        ],
    )
    def test_ambiguous_match_several_ok_true(self, query, choices, expected):
        """Test ambiguous matches allowed when several_ok=True."""
        result = match_arg(query, choices, several_ok=True)
        assert sorted(result) == sorted(expected)


class TestMatchArgNoMatches:
    """Tests for no match scenarios."""

    @pytest.mark.parametrize(
        ("query", "error_pattern"),
        [
            ("orange", "not valid"),
            ("xyz", "is not valid"),
        ],
    )
    def test_no_match_raises_error(self, standard_choices, query, error_pattern):
        """Test that no match raises appropriate ValueError."""
        with pytest.raises(ValueError, match=error_pattern):
            match_arg(query, standard_choices)


class TestMatchArgEdgeCases:
    """Tests for edge cases and error conditions."""

    @pytest.mark.parametrize(
        ("query", "choices", "error_pattern"),
        [
            ("", ["apple", "banana", "cherry"], "not valid"),
            ("app", ["apple1", "apple2", "banana"], "matches multiple choices"),
        ],
    )
    def test_error_conditions(self, query, choices, error_pattern):
        """Test various error conditions."""
        with pytest.raises(ValueError, match=error_pattern):
            match_arg(query, choices)

    def test_case_sensitivity(self):
        """Test that matching is case-sensitive."""
        choices = ["Apple", "apple", "APPLE"]
        result = match_arg("app", choices)
        assert result == "apple"


class TestMatchArgListInput:
    """Tests for list input functionality."""

    def test_match_arg_list_input_several_ok_true(self, standard_choices):
        """Test list input with several_ok=True returns correct list."""
        result = match_arg(["ban", "app"], standard_choices, several_ok=True)
        assert sorted(result) == sorted(["banana", "apple"])

    def test_match_arg_list_input_several_ok_false(self, standard_choices):
        """Test list input with several_ok=False raises error."""
        error_msg = "List input is only allowed when several_ok=True"
        with pytest.raises(ValueError, match=error_msg):
            match_arg(["ban", "app"], standard_choices, several_ok=False)

    def test_match_arg_list_with_ambiguous_element(self, partial_match_choices):
        """Test list with ambiguous element returns all matches when several_ok=True."""
        # "ap" is ambiguous (matches both "apple" and "apricot")
        result = match_arg(["ban", "ap"], partial_match_choices, several_ok=True)
        assert sorted(result) == sorted(["banana", "apple", "apricot"])

    def test_match_arg_list_with_no_match_element(self, standard_choices):
        """Test list with no-match element raises error with clear message."""
        error_msg = "Error in list element 1 \\('xyz'\\).*not valid"
        with pytest.raises(ValueError, match=error_msg):
            match_arg(["ban", "xyz"], standard_choices, several_ok=True)

    def test_match_arg_list_mixed_matches(self):
        """Test list with exact, partial, and multiple matches."""
        choices = ["apple", "apricot", "banana", "blueberry"]
        # "apple" (exact), "ban" (partial), "a" (multiple partial)
        result = match_arg(["apple", "ban", "a"], choices, several_ok=True)
        assert sorted(result) == sorted(["apple", "banana", "apple", "apricot"])

    def test_match_arg_empty_list(self, standard_choices):
        """Test empty list input returns empty list."""
        result = match_arg([], standard_choices, several_ok=True)
        assert result == []

    def test_match_arg_list_with_duplicates(self, standard_choices):
        """Test list input with duplicate arguments."""
        result = match_arg(["ban", "ban", "app"], standard_choices, several_ok=True)
        assert sorted(result) == sorted(["banana", "banana", "apple"])

    def test_match_arg_exact_duplicate_case(self, standard_choices):
        """Test the specific duplicate case requested in comment."""
        result = match_arg(["app", "app"], standard_choices, several_ok=True)
        assert result == ["apple", "apple"]

    @pytest.mark.parametrize(
        ("query_list", "expected"),
        [
            (["apple"], ["apple"]),  # Single element exact match
            (["ban"], ["banana"]),  # Single element partial match
            (["app", "ban"], ["apple", "banana"]),  # Multiple partial matches
        ],
    )
    def test_match_arg_list_various_scenarios(
        self, standard_choices, query_list, expected
    ):
        """Test various list input scenarios."""
        result = match_arg(query_list, standard_choices, several_ok=True)
        assert sorted(result) == sorted(expected)
