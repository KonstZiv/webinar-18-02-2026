"""Rich-based board renderer for the TicTacToe CLI game."""

from __future__ import annotations

from rich.console import Console
from rich.text import Text
from tic_tac_toe_3x3.game.renderers import Renderer
from tic_tac_toe_3x3.logic.models import GameState, Mark

from tictactoe_cli.renderer.symbols import (
    CELL_HEIGHT,
    CELL_WIDTH,
    get_empty_cell,
    get_symbol,
)

_COLS = ("A", "B", "C")
_ROWS = ("1", "2", "3")

_H_SEG = "═" * CELL_WIDTH
_TOP = f"   ╔{_H_SEG}╦{_H_SEG}╦{_H_SEG}╗"
_MID = f"   ╠{_H_SEG}╬{_H_SEG}╬{_H_SEG}╣"
_BOT = f"   ╚{_H_SEG}╩{_H_SEG}╩{_H_SEG}╝"

_MARK_STYLE: dict[str, str] = {
    Mark.CROSS: "bold red",
    Mark.NAUGHT: "bold blue",
}


class RichRenderer(Renderer):
    """Render the game board to the terminal using Rich."""

    def __init__(self, *, console: Console | None = None) -> None:
        self._console = console or Console()

    def render(self, game_state: GameState) -> None:
        """Render the current game state to the terminal."""
        self._console.clear()
        self._print_board(game_state)
        self._print_status(game_state)

    # ------------------------------------------------------------------
    # Board assembly
    # ------------------------------------------------------------------

    def _print_board(self, game_state: GameState) -> None:
        cells = game_state.grid.cells
        console = self._console

        # Column headers
        header = Text("   ", style="dim")
        for col in _COLS:
            header.append(col.center(CELL_WIDTH), style="cyan")
        console.print(header)

        # Top border
        console.print(Text(_TOP, style="white dim"))

        for row_idx in range(3):
            row_chars = [cells[row_idx * 3 + c] for c in range(3)]
            row_lines = [self._cell_lines(ch) for ch in row_chars]
            self._print_row(row_idx, row_chars, row_lines)

            if row_idx < 2:
                console.print(Text(_MID, style="white dim"))

        # Bottom border
        console.print(Text(_BOT, style="white dim"))

    def _print_row(
        self,
        row_idx: int,
        row_chars: list[str],
        row_lines: list[list[str]],
    ) -> None:
        console = self._console
        for line_idx in range(CELL_HEIGHT):
            row_text = Text()

            # Row label on the middle line, spaces otherwise
            if line_idx == CELL_HEIGHT // 2:
                row_text.append(f"{_ROWS[row_idx]}  ", style="cyan")
            else:
                row_text.append("   ")

            row_text.append("║", style="white dim")
            for col_idx in range(3):
                content = row_lines[col_idx][line_idx]
                style = _MARK_STYLE.get(row_chars[col_idx], "")
                row_text.append(content, style=style)
                row_text.append("║", style="white dim")

            console.print(row_text)

    # ------------------------------------------------------------------
    # Cell helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _cell_lines(cell_char: str) -> list[str]:
        """Return 7 lines of ASCII art for a single cell."""
        if cell_char == Mark.CROSS:
            return get_symbol(Mark.CROSS)
        if cell_char == Mark.NAUGHT:
            return get_symbol(Mark.NAUGHT)
        return get_empty_cell()

    # ------------------------------------------------------------------
    # Status line
    # ------------------------------------------------------------------

    def _print_status(self, game_state: GameState) -> None:
        console = self._console
        console.print()

        if game_state.game_over:
            if game_state.tie:
                console.print(Text("  Нічия!", style="bold yellow"))
            else:
                winner = game_state.winner
                style = _MARK_STYLE.get(str(winner), "bold white")
                console.print(Text(f"  Переміг {winner}!", style=style))
        elif game_state.game_not_started:
            console.print(Text("  Нова гра! Хід X", style="bold green"))  # noqa: RUF001
        else:
            mark = game_state.current_mark
            style = _MARK_STYLE.get(str(mark), "bold white")
            console.print(Text(f"  Хід {mark}", style=style))
