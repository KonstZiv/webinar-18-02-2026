"""ASCII-art symbol generator for X and O marks (17x7 block characters)."""

from __future__ import annotations

from tic_tac_toe_3x3.logic.models import Mark

CELL_WIDTH = 17
CELL_HEIGHT = 7


def _center(lines: tuple[str, ...]) -> tuple[str, ...]:
    """Center each line within CELL_WIDTH characters."""
    return tuple(line.center(CELL_WIDTH) for line in lines)


# fmt: off
X_SYMBOL: tuple[str, ...] = _center((
    "███         ███",
    " ████     ████",
    "   ████ ████",
    "     ██████",
    "   ████ ████",
    " ████     ████",
    "███         ███",
))

O_SYMBOL: tuple[str, ...] = _center((
    "█████████████",
    "███         ███",
    "██           ██",
    "██           ██",
    "██           ██",
    "███         ███",
    "█████████████",
))
# fmt: on

EMPTY_CELL: tuple[str, ...] = tuple(" " * CELL_WIDTH for _ in range(CELL_HEIGHT))


def get_symbol(mark: Mark) -> list[str]:
    """Return the 17x7 ASCII-art symbol for the given mark.

    Args:
        mark: The player mark (Mark.CROSS or Mark.NAUGHT).

    Returns:
        A list of 7 strings, each exactly 17 characters wide.
    """
    if mark is Mark.CROSS:
        return list(X_SYMBOL)
    return list(O_SYMBOL)


def get_empty_cell() -> list[str]:
    """Return an empty 17x7 cell (spaces only).

    Returns:
        A list of 7 strings, each exactly 17 characters wide.
    """
    return list(EMPTY_CELL)
