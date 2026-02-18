"""Shared test fixtures."""

import pytest
from tic_tac_toe_3x3.logic.models import GameState, Grid


@pytest.fixture()
def empty_state() -> GameState:
    """Empty board, game not started."""
    return GameState(Grid())


@pytest.fixture()
def mid_game_state() -> GameState:
    """Mid-game board: X played twice, O played once."""
    return GameState(Grid("X 0X     "))


@pytest.fixture()
def x_wins_state() -> GameState:
    """Board where X wins (top row)."""
    return GameState(Grid("XXX00    "))


@pytest.fixture()
def tie_state() -> GameState:
    """Board that ended in a tie."""
    return GameState(Grid("X0XX0X0X0"))
