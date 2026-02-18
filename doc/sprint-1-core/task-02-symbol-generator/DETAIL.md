# Task 02 — Генератор символів X/O: Детальний опис

## Мета
Створити модуль, що повертає візуальні представлення символів X та O у вигляді матриць 17x7 з блоків `█`, готових для вставки в клітинки дошки.

## Що робимо

1. Створити файл `src/tictactoe_cli/renderer/symbols.py`
2. Реалізувати функції/константи для отримання символів:
   - `get_x_symbol() -> list[str]` — повертає 7 рядків по 17 символів кожен
   - `get_o_symbol() -> list[str]` — аналогічно
   - `get_empty_cell() -> list[str]` — порожня клітинка 17x7 (пробіли)
3. Символи будуються з блоків `█` та пробілів
4. **Тести:** створити `tests/test_symbols.py` — розміри матриць, наявність блоків, порожня клітинка

## Як робимо

### Дизайн символу X (17x7)
```
██           ██
 ███       ███
   ███   ███
     █████
   ███   ███
 ███       ███
██           ██
```

### Дизайн символу O (17x7)
```
    █████████
  ███       ███
 ██           ██
 ██           ██
 ██           ██
  ███       ███
    █████████
```

- Розміри клітинки: 17 символів шириною, 7 рядків висотою
- Символи центровані в клітинці
- Кожен рядок padded до рівно 17 символів пробілами
- Тип повернення: `list[str]` де `len(result) == 7` і `len(line) == 17` для кожного рядка

### Архітектурні рішення
- Символи зберігати як константи (tuple of strings) — вони не змінюються
- Функція `get_symbol(mark: Mark) -> list[str]` як єдиний публічний API
- Використовувати `Mark` з `tic_tac_toe_3x3.logic.models` для type safety

## Очікувані результати

- Модуль імпортується без помилок
- `get_symbol(Mark.CROSS)` повертає list з 7 рядків, кожен довжиною 17
- `get_symbol(Mark.NAUGHT)` аналогічно
- Символи візуально впізнавані як X та O в терміналі
- Strict type hints, mypy проходить
- `uv run pytest tests/test_symbols.py` — всі тести зелені

## Як тестувати виконання

```python
# test_symbols.py
from tictactoe_cli.renderer.symbols import get_symbol
from tic_tac_toe_3x3.logic.models import Mark

def test_x_symbol_dimensions():
    symbol = get_symbol(Mark.CROSS)
    assert len(symbol) == 7
    assert all(len(line) == 17 for line in symbol)

def test_o_symbol_dimensions():
    symbol = get_symbol(Mark.NAUGHT)
    assert len(symbol) == 7
    assert all(len(line) == 17 for line in symbol)

def test_x_has_blocks():
    symbol = get_symbol(Mark.CROSS)
    assert any("█" in line for line in symbol)

def test_empty_cell():
    from tictactoe_cli.renderer.symbols import get_empty_cell
    cell = get_empty_cell()
    assert len(cell) == 7
    assert all(line == " " * 17 for line in cell)
```

Візуальна перевірка:
```bash
uv run python -c "
from tictactoe_cli.renderer.symbols import get_symbol
from tic_tac_toe_3x3.logic.models import Mark
print('X:')
for line in get_symbol(Mark.CROSS):
    print(f'|{line}|')
print('O:')
for line in get_symbol(Mark.NAUGHT):
    print(f'|{line}|')
"
```

## Контрольні точки поза тестуванням

1. Символи візуально збалансовані — X симетричний, O округлий
2. При виведенні в термінал символи чітко розрізняються
3. Код відповідає ruff/mypy strict стандартам
