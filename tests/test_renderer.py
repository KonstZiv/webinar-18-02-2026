"""Tests for the Rich board renderer."""

from __future__ import annotations

from io import StringIO

from rich.console import Console
from tic_tac_toe_3x3.logic.models import GameState, Grid

from tictactoe_cli.renderer.board import RichRenderer


def _make_renderer() -> tuple[RichRenderer, StringIO]:
    """Create a renderer with a captured string output."""
    buf = StringIO()
    console = Console(file=buf, force_terminal=True, width=80)
    return RichRenderer(console=console), buf


class TestRenderSmoke:
    """Renderer must not crash for various game states."""

    def test_empty_board(self) -> None:
        renderer, _ = _make_renderer()
        renderer.render(GameState(Grid()))

    def test_mid_game(self, mid_game_state: GameState) -> None:
        renderer, _ = _make_renderer()
        renderer.render(mid_game_state)

    def test_game_over_win(self, x_wins_state: GameState) -> None:
        renderer, _ = _make_renderer()
        renderer.render(x_wins_state)

    def test_game_over_tie(self, tie_state: GameState) -> None:
        renderer, _ = _make_renderer()
        renderer.render(tie_state)


class TestRenderOutput:
    """Verify rendered output contains expected elements."""

    def test_contains_frame_characters(self) -> None:
        renderer, buf = _make_renderer()
        renderer.render(GameState(Grid()))
        output = buf.getvalue()
        assert "╔" in output
        assert "╗" in output
        assert "╚" in output
        assert "╝" in output
        assert "║" in output

    def test_contains_column_headers(self) -> None:
        renderer, buf = _make_renderer()
        renderer.render(GameState(Grid()))
        output = buf.getvalue()
        assert "A" in output
        assert "B" in output
        assert "C" in output

    def test_contains_row_labels(self) -> None:
        renderer, buf = _make_renderer()
        renderer.render(GameState(Grid()))
        output = buf.getvalue()
        assert "1" in output
        assert "2" in output
        assert "3" in output

    def test_contains_block_chars_for_marks(self) -> None:
        renderer, buf = _make_renderer()
        renderer.render(GameState(Grid("X 0      ")))
        output = buf.getvalue()
        assert "█" in output

    def test_empty_board_has_new_game_status(self) -> None:
        renderer, buf = _make_renderer()
        renderer.render(GameState(Grid()))
        output = buf.getvalue()
        assert "Нова гра" in output  # noqa: RUF001

    def test_win_shows_winner(self, x_wins_state: GameState) -> None:
        renderer, buf = _make_renderer()
        renderer.render(x_wins_state)
        output = buf.getvalue()
        assert "Переміг" in output

    def test_tie_shows_draw(self, tie_state: GameState) -> None:
        renderer, buf = _make_renderer()
        renderer.render(tie_state)
        output = buf.getvalue()
        assert "Нічия" in output

    def test_mid_game_shows_current_turn(self, mid_game_state: GameState) -> None:
        renderer, buf = _make_renderer()
        renderer.render(mid_game_state)
        output = buf.getvalue()
        assert "Хід" in output
