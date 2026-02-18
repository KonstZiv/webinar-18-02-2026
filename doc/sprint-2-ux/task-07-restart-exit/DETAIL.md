# Task 07 — Рестарт та вихід: Детальний опис

## Мета
Після завершення партії гравець повинен мати вибір продовження — не перезапускаючи програму.

## Що робимо

1. Додати в `app.py` зовнішній цикл навколо `game.play()`
2. Створити prompt після завершення гри з варіантами:
3. **Тести:** створити `tests/test_post_game.py` — перевірка exit/restart/menu flow з mock input
   - `1. Грати знову` — той самий режим, нова партія
   - `2. Головне меню` — повернутися до вибору режиму
   - `3. Вихід` — завершити програму

## Як робимо

### Структура циклу
```python
def main() -> None:
    while True:
        config = show_main_menu()
        if config is None:  # Вибрано "Вихід"
            break
        while True:
            play_game(config)
            choice = show_post_game_menu()
            if choice == PostGameChoice.PLAY_AGAIN:
                continue
            elif choice == PostGameChoice.MAIN_MENU:
                break
            elif choice == PostGameChoice.EXIT:
                return
```

### Post-game prompt
- Відображати після результату гри (перемога/нічия)
- Використати `rich.prompt.IntPrompt` з 3 варіантами
- Пауза 1-2 секунди перед prompt (щоб гравець побачив результат)

### Обробка Ctrl+C
- `KeyboardInterrupt` → коректний вихід з прощальним повідомленням
- Не повинно показувати traceback

## Очікувані результати

- Після перемоги/нічиї — з'являється меню вибору
- "Грати знову" — нова партія з тими ж налаштуваннями, миттєво
- "Головне меню" — повернення до вибору режиму
- "Вихід" — програма завершується чисто
- Ctrl+C — коректний вихід в будь-який момент
- `uv run pytest tests/test_post_game.py` — всі тести зелені

## Як тестувати виконання

```python
# test_post_game.py
from unittest.mock import patch
from tictactoe_cli.app import main

def test_exit_after_game():
    """Game exits cleanly when user chooses exit."""
    moves = ["b2", "a1", "a3", "c1", "c3"]  # X wins
    with patch("builtins.input", side_effect=[*moves, "3"]):  # 3 = exit
        main()  # Should not raise
```

Ручне тестування: зіграти партію, перевірити всі три варіанти post-game меню.

## Контрольні точки поза тестуванням

1. Перехід між меню та грою — без артефактів на екрані
2. Ctrl+C в будь-який момент — чистий вихід без traceback
3. Стан попередньої гри не впливає на нову партію
