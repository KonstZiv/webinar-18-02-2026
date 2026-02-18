"""Tests for the ASCII-art symbol generator."""

from __future__ import annotations

import pytest
from tic_tac_toe_3x3.logic.models import Mark

from tictactoe_cli.renderer.symbols import (
    CELL_HEIGHT,
    CELL_WIDTH,
    get_empty_cell,
    get_symbol,
)


class TestSymbolDimensions:
    """Every symbol must be exactly CELL_WIDTH x CELL_HEIGHT."""

    @pytest.mark.parametrize("mark", [Mark.CROSS, Mark.NAUGHT])
    def test_row_count(self, mark: Mark) -> None:
        assert len(get_symbol(mark)) == CELL_HEIGHT

    @pytest.mark.parametrize("mark", [Mark.CROSS, Mark.NAUGHT])
    def test_column_width(self, mark: Mark) -> None:
        for line in get_symbol(mark):
            assert len(line) == CELL_WIDTH


class TestSymbolContent:
    """Symbols must contain visible block characters."""

    def test_x_has_blocks(self) -> None:
        symbol = get_symbol(Mark.CROSS)
        assert any("█" in line for line in symbol)

    def test_o_has_blocks(self) -> None:
        symbol = get_symbol(Mark.NAUGHT)
        assert any("█" in line for line in symbol)

    def test_x_is_symmetric_vertically(self) -> None:
        """X symbol should be vertically symmetric (top mirrors bottom)."""
        symbol = get_symbol(Mark.CROSS)
        assert symbol[0] == symbol[6]
        assert symbol[1] == symbol[5]
        assert symbol[2] == symbol[4]

    def test_x_differs_from_o(self) -> None:
        x = get_symbol(Mark.CROSS)
        o = get_symbol(Mark.NAUGHT)
        assert x != o


class TestEmptyCell:
    """Empty cell must be all spaces with correct dimensions."""

    def test_row_count(self) -> None:
        assert len(get_empty_cell()) == CELL_HEIGHT

    def test_column_width(self) -> None:
        for line in get_empty_cell():
            assert len(line) == CELL_WIDTH

    def test_all_spaces(self) -> None:
        for line in get_empty_cell():
            assert line == " " * CELL_WIDTH


class TestGetSymbolReturnsNewList:
    """get_symbol must return a new list each time (not a shared reference)."""

    def test_returns_list(self) -> None:
        result = get_symbol(Mark.CROSS)
        assert isinstance(result, list)

    def test_different_instances(self) -> None:
        a = get_symbol(Mark.CROSS)
        b = get_symbol(Mark.CROSS)
        assert a is not b
