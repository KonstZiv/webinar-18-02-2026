"""Human player implementation using Rich terminal prompts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console
from rich.prompt import Prompt
from tic_tac_toe_3x3.game.players import Player  # type: ignore[import-untyped]

from tictactoe_cli.ui.input import parse_coordinate

if TYPE_CHECKING:
    from tic_tac_toe_3x3.logic.models import GameState, Move


class HumanPlayer(Player):  # type: ignore[misc]
    """A human player that reads moves from terminal input."""

    def __init__(
        self,
        *args: object,
        console: Console | None = None,
        **kwargs: object,
    ) -> None:
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]
        self._console = console or Console()

    def get_move(self, game_state: GameState) -> Move | None:
        """Prompt the user for a move and return it.

        Keeps asking until a valid coordinate for an empty cell is entered.
        Returns None if no possible moves remain.
        """
        if not game_state.possible_moves:
            return None

        while True:
            raw = Prompt.ask(
                f"[yellow]Хід {game_state.current_mark} (a1-c3)[/yellow]",
                console=self._console,
            )
            try:
                index = parse_coordinate(raw)
                return game_state.make_move_to(index)
            except ValueError as exc:
                self._console.print(f"[red]{exc}[/red]")
