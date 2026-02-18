# Task 16 — Coverage gap analysis та інтеграційні тести: Детальний опис

## Мета
Unit-тести вже написані в рамках кожної таски Sprint 1-3. Ця таска закриває прогалини в покритті та додає інтеграційні тести, що перевіряють взаємодію компонентів.

## Що робимо

### 1. Coverage gap analysis
```bash
uv run pytest --cov=tictactoe_cli --cov-report=term-missing
```
- Виявити модулі з coverage < 70%
- Написати додаткові тести для непокритих рядків/бренчів
- Фокус на логіці, не на візуалі (Rich output не потребує 100% coverage)

### 2. Інтеграційні тести
Створити `tests/test_integration.py`:

```python
def test_full_game_human_vs_ai():
    """Full game cycle: menu → game → result → exit."""
    # Mock input: вибір режиму, ходи гравця, post-game exit
    # Assert: no exceptions, game completes

def test_full_game_ai_vs_ai():
    """AI vs AI demo completes without interaction."""
    # Mock input: вибір AI vs AI, post-game exit
    # Assert: game completes in < 10 seconds

def test_restart_flow():
    """Play → restart → play → exit flow."""
    # Mock input: game moves, "play again", more moves, "exit"
    # Assert: two complete games without crash

def test_all_game_modes():
    """Each game mode starts and completes."""
    # Parametrize: HvH, HvAI, AIvAI
```

### 3. Ревізія існуючих тестів
- Перевірити що всі тести з Sprint 1-3 досі проходять
- Видалити дублікати
- Уніфікувати fixtures (винести спільні в `conftest.py`)
- Перевірити що тести ізольовані (не залежать від порядку)

## Як робимо

### Пріоритет покриття
| Модуль | Очікуваний coverage | Фокус |
|--------|-------------------|-------|
| `ui/input.py` | > 90% | Чиста логіка, легко тестувати |
| `animations/physics.py` | > 80% | Математика, edge cases |
| `renderer/symbols.py` | > 90% | Константи + get_symbol |
| `animations/sprites.py` | > 80% | Розміри та структура кадрів |
| `ui/menu.py` | > 70% | Маппінг з mock input |
| `renderer/board.py` | > 50% | Smoke-тести, візуал не тестуємо |
| `animations/*.py` (ефекти) | > 40% | Тільки smoke, решта — візуальна перевірка |

### Структура тестів (фінальна)
```
tests/
├── conftest.py              — shared fixtures (GameState variants)
├── test_symbols.py          — від task-02
├── test_renderer.py         — від task-03
├── test_input.py            — від task-04
├── test_app.py              — від task-05
├── test_menu.py             — від task-06
├── test_post_game.py        — від task-07
├── test_error_handling.py   — від task-08
├── test_place_effect.py     — від task-09
├── test_highlight.py        — від task-10
├── test_sprites.py          — від task-11
├── test_physics.py          — від task-12
├── test_falling.py          — від task-13
├── test_draw_effect.py      — від task-14
├── test_banner.py           — від task-15
└── test_integration.py      — ✨ НОВЕ: end-to-end інтеграційні тести
```

## Очікувані результати

- `uv run pytest` — всі тести зелені (unit + integration)
- `uv run pytest --cov=tictactoe_cli --cov-report=term-missing`:
  - Загальний coverage > 60%
  - Логічні модулі (input, physics, symbols) > 80%
- Тести виконуються менше ніж за 10 секунд
- Жодних warnings або deprecations

## Як тестувати виконання

```bash
uv run pytest -v                                              # Все з деталями
uv run pytest --cov=tictactoe_cli --cov-report=term-missing   # Coverage
uv run pytest --cov=tictactoe_cli --cov-report=html           # HTML звіт
uv run pytest -x                                              # Зупинка на першій помилці
uv run pytest tests/test_integration.py -v                    # Тільки інтеграційні
```

## Контрольні точки поза тестуванням

1. Coverage звіт згенеровано, прогалини документовано
2. Всі fixtures в conftest.py, без дублікатів
3. Тести ізольовані — `pytest --randomly` (якщо встановлено) проходить
4. Інтеграційні тести покривають всі 3 режими гри
