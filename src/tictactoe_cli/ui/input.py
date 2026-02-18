"""Coordinate parsing and validation for human input (a1-c3 format)."""

from __future__ import annotations

_BOARD_SIZE = 3
_COL_MAP: dict[str, int] = {"a": 0, "b": 1, "c": 2}
_VALID_ROWS: set[str] = {"1", "2", "3"}


def parse_coordinate(raw: str) -> int:
    """Convert a chess-style coordinate to a cell index (0-8).

    Args:
        raw: A 2-character string like "a1", "B2", "c3".

    Returns:
        Cell index in 0-8 range (row-major order).

    Raises:
        ValueError: If the coordinate is invalid.
    """
    if len(raw) != 2:
        msg = f"Expected 2 characters, got {len(raw)}: {raw!r}"
        raise ValueError(msg)

    col_char, row_char = raw[0].lower(), raw[1]

    if col_char not in _COL_MAP:
        msg = f"Invalid column {raw[0]!r}, expected a/b/c"
        raise ValueError(msg)

    if row_char not in _VALID_ROWS:
        msg = f"Invalid row {raw[1]!r}, expected 1/2/3"
        raise ValueError(msg)

    return (int(row_char) - 1) * _BOARD_SIZE + _COL_MAP[col_char]
