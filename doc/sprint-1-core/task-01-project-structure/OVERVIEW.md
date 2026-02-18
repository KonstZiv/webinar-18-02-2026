# Task 01 — Структура проєкту, CI та автоматичне ревью

**Спрінт:** 1 — Ядро | **Пріоритет:** High | **Блокує:** task-02, task-03, task-04, task-05

Створити структуру Python-пакета `tictactoe_cli` з pyproject.toml, додати залежності (`tic-tac-toe-3x3`, `rich`), налаштувати `ruff`, `mypy`, `pytest`. Налаштувати GitHub Actions CI pipeline (lint + type check + tests) та автоматичне AI-ревью PR через `ai-reviewbot`. Після завершення — `uv sync` працює, пакет імпортується, CI проходить на кожен push/PR.
