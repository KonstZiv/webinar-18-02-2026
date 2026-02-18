# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TicTacToe CLI — a console Tic-Tac-Toe game with Rich visualization and cinematic animation effects.
Built on top of the [`tic-tac-toe-3x3`](https://pypi.org/project/tic-tac-toe-3x3/) library (installed as dependency), which provides the game engine, AI opponent (minimax), and base abstractions (`Renderer`, `Player`, `GameState`).

This project extends the library with a full interactive CLI client: Rich-rendered board, animated symbol placement, falling symbols with rotation physics, win/draw effects.

## Commands

```bash
uv sync                              # Install dependencies
uv run python -m tictactoe_cli       # Run the game
uv run ruff check src tests          # Lint
uv run ruff format src tests         # Format
uv run pytest                        # Run all tests
uv run pytest tests/test_foo.py      # Run a single test file
uv run pytest -k "test_name"         # Run a single test by name
```

## Tech Stack

- Python 3.14, dependency management via `uv`
- `tic-tac-toe-3x3` — game engine (Grid, GameState, Mark, Move, TicTacToe/AsyncTicTacToe, Player/AsyncPlayer, Renderer/AsyncRenderer, MinimaxComputerPlayer)
- `Rich` — terminal UI rendering
- `curses` / Rich Live / ANSI — animations
- `ruff` — linting & formatting, `mypy` — type checking, `pytest` — testing

## Architecture

### Library layer (`tic-tac-toe-3x3`, read-only dependency)

- `logic.models` — `Mark` (StrEnum: "X"/"0"), `Grid` (9-char string), `GameState` (cached properties: `current_mark`, `game_over`, `winner`, `winning_cells`, `possible_moves`, `tie`), `Move`
- `game.engine` — `TicTacToe` and `AsyncTicTacToe` — game loop orchestrators. Accept `player1`, `player2`, `renderer`, optional `error_handler`
- `game.players` — abstract `Player`/`AsyncPlayer` (must implement `get_move`), `ComputerPlayer`/`AsyncComputerPlayer` (adds delay), `MinimaxComputerPlayer`, `RandomComputerPlayer`
- `game.renderers` — abstract `Renderer`/`AsyncRenderer` (must implement `render(game_state)`)
- `logic.minimax` — `find_best_move(game_state)` for AI

### Application layer (`tictactoe_cli`, this project)

Target structure (per PROJECT_DESCRIPTION.md):
```
tictactoe_cli/
├── renderer/
│   ├── board.py        — Rich renderer (ASCII-art 17×7 cells, double-line frames)
│   ├── symbols.py      — X/O symbol generator using █ blocks
│   └── effects.py      — Animation effects
├── ui/
│   ├── menu.py         — Main menu, mode selection
│   └── input.py        — Input handling (coordinates a1..c3)
├── animations/
│   ├── sprites.py      — Rotation sprites (frame sets 17×7)
│   ├── physics.py      — 2D physics: gravity, collisions, bounding box
│   ├── falling.py      — Falling symbols orchestration
│   ├── highlight.py    — Winning line highlight
│   ├── celebration.py  — Victory effect (banner + effects)
│   └── draw.py         — Draw effect (dissolve)
├── app.py              — Entry point, Game Runner
└── __main__.py         — Module entry point
```

### Key extension points

To integrate with the library, this project must:
1. Subclass `Renderer` (or `AsyncRenderer`) — implement `render(game_state: GameState)` for Rich-based board display
2. Subclass `Player` (or `AsyncPlayer`) — implement `get_move(game_state: GameState) -> Move | None` for human input (a1..c3 coordinate mapping to cell index 0-8)
3. Wire them into `TicTacToe(player1, player2, renderer).play()`

### Board coordinate mapping

User input uses chess-like notation (a1, b2, c3). Columns A/B/C map to grid indices modulo 3, rows 1/2/3 map to grid indices divided by 3. Grid cells are a flat 9-char string indexed 0-8 (row-major: top-left=0, bottom-right=8).

## Game Modes

- Human vs Human — two players on one terminal
- Human vs AI — player vs `MinimaxComputerPlayer`
- AI vs AI — demo mode with two AI players
