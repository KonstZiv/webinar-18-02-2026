# Task 05 — Game Runner: Детальний опис

## Мета
Зібрати всі компоненти Sprint 1 в працюючу гру — від запуску до завершення партії.

## Що робимо

1. Створити `src/tictactoe_cli/app.py` — головний модуль запуску
2. Оновити `src/tictactoe_cli/__main__.py` — виклик app
3. **Тести:** створити `tests/test_app.py` — smoke test з мокнутим введенням (повна гра без crash)

### app.py
```python
def main() -> None:
    """Entry point for the TicTacToe CLI game."""
    # 1. Створити гравців
    player1 = HumanPlayer(Mark.CROSS)
    player2 = MinimaxComputerPlayer(Mark.NAUGHT)

    # 2. Створити рендерер
    renderer = RichRenderer()

    # 3. Створити та запустити гру
    game = TicTacToe(
        player1=player1,
        player2=player2,
        renderer=renderer,
        error_handler=handle_error,
    )
    game.play()
```

### __main__.py
```python
from tictactoe_cli.app import main
main()
```

### Error handler
- Проста функція що виводить помилку через Rich console
- Передається як `error_handler` в `TicTacToe`

## Як робимо

### Інтеграція з бібліотекою
- `TicTacToe` з `tic_tac_toe_3x3.game.engine` — приймає player1, player2, renderer
- `.play()` — запускає головний цикл:
  1. `renderer.render(game_state)` — відображає дошку
  2. Якщо `game_over` — break
  3. Поточний гравець робить хід → новий `game_state`
  4. Повторити

### Flow гри
1. Запуск → відображається порожня дошка
2. Гравець вводить координату → символ X з'являється
3. AI "думає" (0.25с delay) → символ O з'являється
4. Повторюється до перемоги або нічиї
5. Останній `render()` показує фінальний стан з результатом

### Поточні обмеження (Sprint 1)
- Тільки один режим: Human (X) vs AI (O)
- Немає меню (додається в Sprint 2)
- Немає анімацій (додаються в Sprint 3)
- Після завершення — програма завершується (рестарт в Sprint 2)

## Очікувані результати

- `uv run python -m tictactoe_cli` — запускає повноцінну гру
- Гравець може зіграти повну партію від початку до кінця
- AI відповідає розумними ходами (minimax)
- При невалідному введенні — повідомлення про помилку, гра продовжується
- При перемозі/нічиї — відображається результат, програма завершується
- `uv run pytest tests/test_app.py` — smoke test зелений

## Як тестувати виконання

### Автоматичне тестування
```python
# test_app.py — smoke test з мокнутим введенням
from unittest.mock import patch
from tictactoe_cli.app import main

def test_game_runs_without_crash():
    """Simulated game completes without exceptions."""
    moves = ["b2", "a1", "c3", "a3", "a2", "c2", "b1", "b3", "c1"]
    with patch("builtins.input", side_effect=moves):
        main()  # Should complete without error
```

### Ручне тестування
1. Запустити `uv run python -m tictactoe_cli`
2. Зіграти повну партію, перевірити що AI відповідає
3. Спробувати невалідне введення (`z9`, `aa`, пустий рядок)
4. Спробувати хід в зайняту клітинку
5. Довести гру до перемоги X, перемоги O (складно проти minimax), і нічиї

## Контрольні точки поза тестуванням

1. Гра не зависає на жодному етапі
2. AI не крашить при будь-якому стані дошки
3. Error handler виводить зрозумілі повідомлення
4. Фінальне відображення дошки показує правильний стан
5. Програма коректно завершується (exit code 0)
