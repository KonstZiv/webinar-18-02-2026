"""Tests for coordinate parsing and validation."""

from __future__ import annotations

import pytest

from tictactoe_cli.ui.input import parse_coordinate


class TestValidCoordinates:
    """All 9 valid coordinates must map to correct cell indices."""

    @pytest.mark.parametrize(
        ("coord", "expected"),
        [
            ("a1", 0),
            ("b1", 1),
            ("c1", 2),
            ("a2", 3),
            ("b2", 4),
            ("c2", 5),
            ("a3", 6),
            ("b3", 7),
            ("c3", 8),
        ],
    )
    def test_lowercase(self, coord: str, expected: int) -> None:
        assert parse_coordinate(coord) == expected

    @pytest.mark.parametrize(
        ("coord", "expected"),
        [
            ("A1", 0),
            ("B2", 4),
            ("C3", 8),
            ("A3", 6),
            ("C1", 2),
        ],
    )
    def test_uppercase(self, coord: str, expected: int) -> None:
        assert parse_coordinate(coord) == expected


class TestInvalidCoordinates:
    """Invalid input must raise ValueError."""

    @pytest.mark.parametrize(
        "coord",
        [
            "",
            "a",
            "1",
            "d1",
            "a4",
            "a0",
            "ab",
            "11",
            "abc",
            " a1",
            "a1 ",
        ],
    )
    def test_raises_value_error(self, coord: str) -> None:
        with pytest.raises(ValueError):
            parse_coordinate(coord)
