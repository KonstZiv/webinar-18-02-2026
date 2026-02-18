# Task 06 — Головне меню: Детальний опис

## Мета
Реалізувати головне меню з вибором режиму гри, яке з'являється при запуску і дозволяє обрати тип партії.

## Що робимо

1. Створити `src/tictactoe_cli/ui/menu.py`
2. Функція `show_main_menu() -> GameConfig` — відображає меню, повертає конфігурацію
3. Оновити `app.py` — перед запуском гри показувати меню
4. **Тести:** створити `tests/test_menu.py` — маппінг вибору на `GameConfig` (з mock input)

### Меню
```
╔══════════════════════════════════╗
║     TIC-TAC-TOE  CLI  v0.1      ║
╠══════════════════════════════════╣
║                                  ║
║   1. Human vs Human              ║
║   2. Human vs AI                 ║
║   3. AI vs AI (Demo)             ║
║                                  ║
║   0. Вихід                       ║
║                                  ║
╚══════════════════════════════════╝
```

### GameConfig
```python
@dataclass(frozen=True)
class GameConfig:
    player1_type: PlayerType  # HUMAN | AI
    player2_type: PlayerType
    player1_mark: Mark
```

## Як робимо

- Використати `rich.panel.Panel` для рамки меню
- `rich.prompt.IntPrompt.ask()` для вибору пункту
- Валідація вибору: 0-3, інші значення → повторний запит
- Для Human vs AI — додатковий prompt: "Граєте за X чи O?"
- Повертає `GameConfig` що використовується в `app.py` для створення гравців

### Маппінг режимів на гравців
| Режим | player1 | player2 |
|-------|---------|---------|
| Human vs Human | `HumanPlayer(X)` | `HumanPlayer(O)` |
| Human vs AI | `HumanPlayer(вибір)` | `MinimaxComputerPlayer(інший)` |
| AI vs AI | `MinimaxComputerPlayer(X)` | `RandomComputerPlayer(O)` |

## Очікувані результати

- При запуску — меню з пунктами замість прямого запуску гри
- Вибір 1/2/3 → запуск відповідного режиму
- Вибір 0 → вихід з програми
- Некоректне введення → повторний запит
- `uv run pytest tests/test_menu.py` — всі тести зелені

## Як тестувати виконання

```python
# test_menu.py
from unittest.mock import patch
from tictactoe_cli.ui.menu import show_main_menu, PlayerType

def test_human_vs_ai_selection():
    with patch("rich.prompt.IntPrompt.ask", side_effect=[2, 1]):  # mode=2, mark=X
        config = show_main_menu()
        assert config.player1_type == PlayerType.HUMAN
        assert config.player2_type == PlayerType.AI
```

Ручне тестування: запустити гру, перевірити що кожен пункт меню працює.

## Контрольні точки поза тестуванням

1. Меню візуально привабливе, текст вирівняний
2. Вибір режиму інтуїтивно зрозумілий
3. AI vs AI демо працює автоматично (гравець тільки спостерігає)
