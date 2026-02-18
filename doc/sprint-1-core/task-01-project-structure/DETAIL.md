# Task 01 — Структура проєкту, CI та автоматичне ревью: Детальний опис

## Мета
Ініціалізувати проєкт з правильною структурою пакетів, залежностями, інструментами якості коду, CI pipeline та автоматичним AI-ревью pull requests.

## Що робимо

### 1. pyproject.toml

- Додати залежності: `rich`
- Додати dev-залежності: `ruff`, `mypy`, `pytest`, `pytest-cov`
- Налаштувати секції `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]`
- Додати entry point для `__main__.py`

### 2. Структура пакета

```
src/tictactoe_cli/
├── __init__.py
├── __main__.py
├── renderer/
│   └── __init__.py
├── ui/
│   └── __init__.py
└── animations/
    └── __init__.py

tests/
├── __init__.py
└── conftest.py
```

### 3. `__main__.py`

Мінімальна точка входу, що виводить "TicTacToe CLI" (placeholder).

### 4. pytest — базова конфігурація

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

Створити `tests/conftest.py` з базовими fixtures (порожній `GameState`, стан перемоги, стан нічиї).
Створити `tests/test_smoke.py` — мінімальний тест що пакет імпортується.

### 5. GitHub Actions CI pipeline

Створити `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install 3.14

      - name: Install dependencies
        run: uv sync

      - name: Lint
        run: uv run ruff check src tests

      - name: Format check
        run: uv run ruff format --check src tests

      - name: Type check
        run: uv run mypy --strict src

      - name: Tests
        run: uv run pytest --tb=short -q
```

### 6. Автоматичне AI-ревью PR через ai-reviewbot

Створити `.github/workflows/ai-review.yml`:

```yaml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: KonstZiv/ai-code-reviewer@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          google_api_key: ${{ secrets.GOOGLE_API_KEY }}
```

**Необхідні secrets у GitHub repo settings:**
- `GOOGLE_API_KEY` — API key для Google Gemini (потрібно додати вручну в Settings → Secrets → Actions)
- `GITHUB_TOKEN` — надається автоматично GitHub Actions

**Що робить ai-reviewbot:**
- Аналізує diff кожного PR через Google Gemini AI
- Залишає inline-коментарі з категоризацією: Critical / Warning / Info
- Перевіряє security, code quality, best practices
- Коментарі мають кнопку one-click apply для швидкого виправлення
- Вартість: ~$0.002 за ревью (Gemini 2.5 Flash)

**Опціональні змінні середовища (env в workflow):**

| Змінна | Опис | Default |
|--------|------|---------|
| `LANGUAGE` | Мова відповідей (ISO 639) | `en` |
| `GEMINI_MODEL` | Модель Gemini | `gemini-2.5-flash` |

Для українських коментарів додати `LANGUAGE: uk`:
```yaml
      - uses: KonstZiv/ai-code-reviewer@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          google_api_key: ${{ secrets.GOOGLE_API_KEY }}
        env:
          LANGUAGE: uk
```

## Як робимо

- Використовуємо `src/` layout для пакета (стандарт для Python проєктів)
- В pyproject.toml — `[project.scripts]` секція для CLI entry point
- ruff: default rules, target Python 3.14
- mypy: `strict = true`
- pytest: `testpaths = ["tests"]`, `pythonpath = ["src"]`
- CI: два окремі workflow — `ci.yml` (lint/test, на push+PR) та `ai-review.yml` (AI ревью, тільки PR)

## Очікувані результати

- `uv sync` — без помилок
- `uv run python -m tictactoe_cli` — друкує placeholder текст
- `uv run python -c "from tictactoe_cli import __version__"` — без помилок
- `uv run ruff check src tests` — без помилок
- `uv run mypy --strict src` — без помилок
- `uv run pytest` — smoke test проходить
- Push в main → GitHub Actions CI проходить зелено
- Створення PR → CI проходить + ai-reviewbot залишає inline-коментарі

## Як тестувати виконання

```bash
# Локально
uv sync
uv run python -m tictactoe_cli          # Має вивести placeholder
uv run python -c "import tictactoe_cli"  # Не має впасти
uv run ruff check src tests              # 0 errors
uv run ruff format --check src tests     # 0 errors
uv run mypy --strict src                 # Success
uv run pytest                            # 1 test passed

# CI
# 1. Push в main → перевірити Actions tab → ci.yml green
# 2. Створити тестовий PR → перевірити:
#    - ci.yml проходить
#    - ai-review.yml запускається
#    - ai-reviewbot залишає коментарі на PR
```

## Контрольні точки поза тестуванням

1. pyproject.toml містить всі залежності та налаштування ruff/mypy/pytest
2. Структура тек відповідає архітектурі з PROJECT_DESCRIPTION.md
3. Всі `__init__.py` файли на місці (пакети імпортуються)
4. `.gitignore` оновлено при потребі
5. `.github/workflows/ci.yml` — валідний YAML, містить lint + format + type check + tests
6. `.github/workflows/ai-review.yml` — валідний YAML, використовує `KonstZiv/ai-code-reviewer@v1`
7. `GOOGLE_API_KEY` secret додано в repo settings (або задокументовано що потрібно додати)
8. Тестовий PR отримує автоматичне AI-ревью з inline-коментарями
