"""Smoke tests: package imports and basic sanity checks."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tic_tac_toe_3x3.logic.models import GameState


def test_package_imports() -> None:
    """Package can be imported without errors."""
    import tictactoe_cli

    assert hasattr(tictactoe_cli, "__version__")


def test_version_is_string() -> None:
    """Version is a valid string."""
    from tictactoe_cli import __version__

    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_fixtures_valid(
    empty_state: GameState,
    x_wins_state: GameState,
    tie_state: GameState,
) -> None:
    """Shared fixtures produce valid GameState objects."""
    assert empty_state.game_not_started
    assert not empty_state.game_over

    assert x_wins_state.game_over
    assert x_wins_state.winner is not None

    assert tie_state.game_over
    assert tie_state.tie
