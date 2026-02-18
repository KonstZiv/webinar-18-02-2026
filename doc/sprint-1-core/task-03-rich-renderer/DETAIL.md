# Task 03 — Rich Renderer дошки: Детальний опис

## Мета
Створити повноцінний рендерер дошки, що наслідує абстрактний `Renderer` з бібліотеки `tic-tac-toe-3x3` і відображає стан гри через Rich у терміналі.

## Що робимо

1. Створити `src/tictactoe_cli/renderer/board.py`
2. Клас `RichRenderer(Renderer)` з методом `render(game_state: GameState) -> None`
3. **Тести:** створити `tests/test_renderer.py` — smoke-тести для різних `GameState` (empty, mid-game, win, tie)
4. Відображення включає:
   - Подвійні Unicode-рамки (`╔═╗║╚╝╦╩╠╣╬`)
   - 3x3 клітинки, кожна 17x7 символів
   - Координати: колонки A, B, C зверху; ряди 1, 2, 3 зліва
   - Кольори: X — `bold red`, O — `bold blue`, рамки — `white`/`dim`
   - Координати — `cyan`
   - Рядок статусу: чий хід або результат гри

## Як робимо

### Структура дошки (візуально)
```
       A                 B                 C
   ╔═════════════════╦═════════════════╦═════════════════╗
   ║                 ║                 ║                 ║
   ║                 ║                 ║                 ║
   ║                 ║                 ║                 ║
1  ║     CELL 0      ║     CELL 1      ║     CELL 2      ║
   ║                 ║                 ║                 ║
   ║                 ║                 ║                 ║
   ║                 ║                 ║                 ║
   ╠═════════════════╬═════════════════╬═════════════════╣
   ║                 ║                 ║                 ║
   ║                 ║                 ║                 ║
   ║                 ║                 ║                 ║
2  ║     CELL 3      ║     CELL 4      ║     CELL 5      ║
   ║                 ║                 ║                 ║
   ║                 ║                 ║                 ║
   ║                 ║                 ║                 ║
   ╠═════════════════╬═════════════════╬═════════════════╣
   ║                 ║                 ║                 ║
   ║                 ║                 ║                 ║
   ║                 ║                 ║                 ║
3  ║     CELL 6      ║     CELL 7      ║     CELL 8      ║
   ║                 ║                 ║                 ║
   ║                 ║                 ║                 ║
   ║                 ║                 ║                 ║
   ╚═════════════════╩═════════════════╩═════════════════╝
```

### Алгоритм рендерингу
1. Отримати `game_state.grid.cells` — рядок з 9 символів
2. Для кожної клітинки: якщо `"X"` — `get_symbol(Mark.CROSS)`, `"0"` — `get_symbol(Mark.NAUGHT)`, `" "` — `get_empty_cell()`
3. Зібрати рядки дошки: для кожного з 3 рядів дошки об'єднати 7 рядків символів з роздільниками `║`
4. Додати верхню, середні та нижню рамки
5. Додати координати
6. Вивести через `rich.console.Console`
7. Під дошкою — рядок статусу:
   - `game_state.game_not_started` → "Нова гра! Хід X"
   - `game_state.game_over` + winner → "Переміг {winner}!"
   - `game_state.tie` → "Нічия!"
   - інакше → "Хід {current_mark}"

### Архітектурні рішення
- `Console` створюється один раз в `__init__`
- Перед кожним `render()` — `console.clear()` для оновлення екрану
- Використовувати `rich.text.Text` для кольорового виводу або прямий markup `[bold red]...[/]`

## Очікувані результати

- `RichRenderer().render(GameState(Grid()))` — виводить порожню дошку з рамками та координатами
- `RichRenderer().render(GameState(Grid("X   0   X")))` — показує X та O у правильних клітинках з кольорами
- Статус під дошкою відповідає поточному стану гри
- `uv run pytest tests/test_renderer.py` — всі smoke-тести зелені

## Як тестувати виконання

```python
# test_renderer.py
from tictactoe_cli.renderer.board import RichRenderer
from tic_tac_toe_3x3.logic.models import GameState, Grid

def test_render_empty_board(capsys):
    """Renderer does not crash on empty board."""
    renderer = RichRenderer()
    renderer.render(GameState(Grid()))
    # No exception = pass

def test_render_mid_game(capsys):
    """Renderer does not crash on mid-game state."""
    renderer = RichRenderer()
    renderer.render(GameState(Grid("X 0X     ")))

def test_render_game_over(capsys):
    """Renderer does not crash on finished game."""
    renderer = RichRenderer()
    renderer.render(GameState(Grid("XXX00    ")))
```

Візуальна перевірка:
```bash
uv run python -c "
from tictactoe_cli.renderer.board import RichRenderer
from tic_tac_toe_3x3.logic.models import GameState, Grid
r = RichRenderer()
r.render(GameState(Grid('X 0 X 0  ')))
"
```

## Контрольні точки поза тестуванням

1. Дошка виглядає акуратно в терміналі шириною 80+ символів
2. Кольори X (червоний) та O (синій) чітко розрізняються
3. Рамки не ламаються — всі кути та перетини на місці
4. Координати вирівняні з відповідними колонками/рядами
