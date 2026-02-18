# Task 04 — Обробка введення: Детальний опис

## Мета
Реалізувати Human Player, що приймає введення гравця у форматі шахових координат (`a1`, `b2`, `c3`), валідує його та повертає відповідний `Move`.

## Що робимо

1. Створити `src/tictactoe_cli/ui/input.py` — парсинг та валідація координат
2. Створити `src/tictactoe_cli/ui/players.py` — клас `HumanPlayer(Player)`
3. **Тести:** створити `tests/test_input.py` — параметризовані тести для всіх 9 координат + edge cases

### Модуль input.py
- `parse_coordinate(raw: str) -> int` — конвертує координату в індекс клітинки
  - `a1` → 0, `b1` → 1, `c1` → 2
  - `a2` → 3, `b2` → 4, `c2` → 5
  - `a3` → 6, `b3` → 7, `c3` → 8
- Валідація: `ValueError` при некоректному введенні
- Case-insensitive: `A1` == `a1`

### Клас HumanPlayer
```python
class HumanPlayer(Player):
    def get_move(self, game_state: GameState) -> Move | None:
        # 1. Запитати введення через Rich prompt
        # 2. Спарсити координату → cell_index
        # 3. Повернути game_state.make_move_to(cell_index)
```

## Як робимо

### Маппінг координат
```
Формула: index = (row - 1) * 3 + col_index
де col_index: a=0, b=1, c=2
   row: 1, 2, 3

Таблиця:
     A(0)  B(1)  C(2)
1:   0     1     2
2:   3     4     5
3:   6     7     8
```

### Валідація
- Рядок має бути рівно 2 символи
- Перший символ: `a`, `b`, `c` (або uppercase)
- Другий символ: `1`, `2`, `3`
- Все інше — `ValueError` з описовим повідомленням

### Input prompt
- Використовувати `rich.prompt.Prompt.ask()` з підказкою формату
- Prompt: `"Ваш хід (a1-c3)"` з кольором `yellow`

## Очікувані результати

- `parse_coordinate("a1")` → `0`
- `parse_coordinate("c3")` → `8`
- `parse_coordinate("B2")` → `4` (case-insensitive)
- `parse_coordinate("d1")` → `ValueError`
- `parse_coordinate("")` → `ValueError`
- `parse_coordinate("a4")` → `ValueError`
- `HumanPlayer` інтегрується з `TicTacToe` engine
- `uv run pytest tests/test_input.py` — всі тести зелені

## Як тестувати виконання

```python
# test_input.py
import pytest
from tictactoe_cli.ui.input import parse_coordinate

@pytest.mark.parametrize("coord,expected", [
    ("a1", 0), ("b1", 1), ("c1", 2),
    ("a2", 3), ("b2", 4), ("c2", 5),
    ("a3", 6), ("b3", 7), ("c3", 8),
    ("A1", 0), ("B2", 4), ("C3", 8),  # case-insensitive
])
def test_valid_coordinates(coord, expected):
    assert parse_coordinate(coord) == expected

@pytest.mark.parametrize("coord", [
    "", "a", "1", "d1", "a4", "a0", "ab", "11", "abc", " a1", "a1 ",
])
def test_invalid_coordinates(coord):
    with pytest.raises(ValueError):
        parse_coordinate(coord)
```

## Контрольні точки поза тестуванням

1. Введення працює в реальному терміналі (не тільки в тестах)
2. Prompt візуально зрозумілий — гравець розуміє що вводити
3. При помилці гра не крашить, а запитує повторно (в контексті Game Runner)
