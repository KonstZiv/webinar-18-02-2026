# Task 08 — Повідомлення про помилки введення: Детальний опис

## Мета
Зробити обробку помилок введення зручною і інформативною — гравець завжди розуміє що пішло не так і як виправити.

## Що робимо

1. Оновити `ui/input.py` — деталізовані повідомлення для різних типів помилок
2. Оновити error handler в `app.py` — Rich-стилізований вивід помилок
3. Реалізувати повторний запит введення при помилці (retry loop в `HumanPlayer.get_move`)
4. **Тести:** створити `tests/test_error_handling.py` — перевірка що error messages описові та match очікуваним патернам

### Типи помилок та повідомлення

| Ситуація | Повідомлення |
|----------|-------------|
| Пустий рядок | "Введіть координату у форматі a1-c3" |
| Невалідний формат | "'{input}' — невірний формат. Використовуйте a1-c3" |
| Зайнята клітинка | "Клітинка {coord} вже зайнята. Оберіть іншу" |
| Хід поза дошкою | "Координата '{input}' поза межами дошки" |

## Як робимо

### Стилізація повідомлень
- Використати `rich.panel.Panel` з `border_style="red"` для помилок
- Іконка `[bold red]✗[/]` перед текстом помилки
- Підказка формату `[dim](Формат: a1, b2, c3)[/dim]` під повідомленням

### Retry loop
```python
class HumanPlayer(Player):
    def get_move(self, game_state: GameState) -> Move | None:
        while True:
            try:
                raw = Prompt.ask("[yellow]Ваш хід[/]")
                index = parse_coordinate(raw)
                return game_state.make_move_to(index)
            except ValueError as e:
                self.console.print(f"[red]✗ {e}[/red]")
            except InvalidMove as e:
                self.console.print(f"[red]✗ {e}[/red]")
```

### Інтеграція з error_handler
- `error_handler` в `TicTacToe` — для помилок що прокидаються з engine
- Retry loop в `HumanPlayer` — для помилок введення (не доходять до engine)

## Очікувані результати

- Будь-яке невалідне введення → червоне повідомлення + повторний запит
- Спроба ходу в зайняту клітинку → повідомлення + повторний запит
- Після 10 послідовних помилок гра не крашить
- Повідомлення зрозумілі — навіть новий гравець розуміє що робити
- `uv run pytest tests/test_error_handling.py` — всі тести зелені

## Як тестувати виконання

```python
# test_error_handling.py
from unittest.mock import patch
from tictactoe_cli.ui.input import parse_coordinate
import pytest

@pytest.mark.parametrize("bad_input,expected_msg", [
    ("", "формат"),
    ("z9", "формат"),
    ("aa", "формат"),
    ("a4", "межами"),
])
def test_error_messages_are_descriptive(bad_input, expected_msg):
    with pytest.raises(ValueError, match=expected_msg):
        parse_coordinate(bad_input)
```

Ручне тестування: під час гри ввести 5+ різних невалідних значень підряд.

## Контрольні точки поза тестуванням

1. Повідомлення про помилки візуально виділяються (червоний колір)
2. Після помилки гра повертається в нормальний стан (prompt з'являється знову)
3. Помилки не забруднюють екран — максимум 2-3 рядки на помилку
