# Task 10 — Highlight виграшної лінії: Детальний опис

## Мета
Візуально виділити три клітинки, що утворюють виграшну лінію, мигаючим зеленим кольором.

## Що робимо

1. Створити `src/tictactoe_cli/animations/highlight.py`
2. **Тести:** додати `tests/test_highlight.py` — перевірка коректних winning cells, відсутність highlight при нічиї
3. Функція `highlight_winning_line(console, game_state, renderer)`:
   - Отримує `game_state.winning_cells` — список з 3 індексів
   - Перемальовує дошку з чергуванням: зелений/звичайний колір для winning cells
   - 2-3 цикли мигання, кожен ~300ms

## Як робимо

### Алгоритм
1. `cells = game_state.winning_cells` → наприклад `[0, 1, 2]`
2. Для `i` в range(6) (3 повних мигання):
   - Якщо `i` парне → winning cells зеленим (`bold green`)
   - Якщо `i` непарне → winning cells звичайним кольором
   - Перемалювати дошку через `Live`
   - `time.sleep(0.3)`

### Модифікація рендерера
- `RichRenderer.render()` приймає опціональний `highlight_cells: list[int] = []`
- Якщо клітинка в `highlight_cells` → використовувати `bold green` замість звичайного кольору
- Можна реалізувати як окремий метод `render_with_highlight(game_state, cells, color)`

### Технічні деталі
- `rich.live.Live` для flicker-free мигання
- Зелений: `[bold green]█[/bold green]` для блоків символу
- Звичайний: `[bold red]█[/bold red]` для X, `[bold blue]█[/bold blue]` для O

## Очікувані результати

- При перемозі — три клітинки мигають зеленим 2-3 рази
- Мигання чітко видно (контраст між зеленим та звичайним кольором)
- Після мигання — клітинки залишаються зеленими (або повертаються до звичайного)
- При нічиї — highlight не викликається

## Як тестувати виконання

```python
# test_highlight.py
from tictactoe_cli.animations.highlight import highlight_winning_line
from tic_tac_toe_3x3.logic.models import GameState, Grid

def test_highlight_identifies_correct_cells():
    """Winning cells are correctly identified for highlighting."""
    state = GameState(Grid("XXX00    "))
    assert state.winning_cells == [0, 1, 2]

def test_no_highlight_on_tie():
    """No highlight when game is a tie."""
    state = GameState(Grid("X0XX0000X"))
    assert state.winning_cells == []
```

Візуальна перевірка: довести гру до перемоги, спостерігати мигання.

## Контрольні точки поза тестуванням

1. Мигання помітне — зелений чітко відрізняється від червоного/синього
2. Мигання не занадто швидке і не занадто повільне (помітне, але не дратує)
3. Highlight працює для всіх 8 можливих виграшних ліній (3 рядки, 3 стовпці, 2 діагоналі)
4. Рамки дошки не мигають — тільки вміст клітинок
