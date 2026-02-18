# Task 13 — Falling Symbols: Детальний опис

## Мета
Реалізувати повну анімацію падіння символів з дошки — каскад, обертання, колізії, сліди, фінал. Це центральний візуальний ефект проєкту.

## Що робимо

1. Створити `src/tictactoe_cli/animations/falling.py`
2. Клас `FallingSymbolsAnimation` — оркестратор всієї анімації
3. Інтеграція: sprite + physics + rendering в єдиний loop
4. **Тести:** створити `tests/test_falling.py` — всі об'єкти деактивуються, cascade delays різні

## Як робимо

### Архітектура
```python
class FallingSymbolsAnimation:
    def __init__(
        self,
        game_state: GameState,
        console: Console,
        board_layout: BoardLayout,  # позиції клітинок та рамок на екрані
    ):
        self.objects: list[FallingSymbolData] = []
        self.physics = PhysicsEngine(
            obstacles=board_layout.frame_obstacles,
            screen_height=console.height,
        )

    def run(self) -> None:
        """Execute the full falling animation."""
        self._init_objects()
        with Live(console=self.console, refresh_per_second=20) as live:
            while any(obj.falling.active for obj in self.objects):
                self._update_frame()
                frame = self._render_frame()
                live.update(frame)
                time.sleep(1 / 20)  # 20 FPS
```

### FallingSymbolData
```python
@dataclass
class FallingSymbolData:
    falling: FallingObject       # фізичний стан
    mark: Mark                   # X або O
    frames: tuple[list[str], ...]  # sprite sheet
    start_delay: float           # затримка перед початком падіння
    trail: list[TrailPoint]      # точки сліду
```

### Каскад
- Символи починають падати з затримкою: `i * 0.15` секунд
- Порядок: зліва-направо, зверху-вниз (або рандомний для ефекту)
- Поки символ "чекає" — він залишається на місці на дошці

### Сліди (trails)
```python
@dataclass
class TrailPoint:
    x: float
    y: float
    age: int       # кількість кадрів від створення
    max_age: int   # після цього — зникає
```
- Кожен кадр → додати поточну позицію як `TrailPoint`
- Рендеринг сліду: `age 0` → `dim`, `age 1` → `darker`, `age 2+` → видалити
- Використовувати `░`, `▒`, `▓` або Rich dim/darker стилі

### Рендеринг кадру
1. Створити порожній "екран" (список рядків по висоті терміналу)
2. Намалювати рамки дошки (вони залишаються на місці поки символи падають)
3. Намалювати сліди (dim символи)
4. Намалювати кожен активний об'єкт:
   - Взяти поточний кадр зі sprite sheet (`frames[angle]`)
   - Розмістити на екрані за позицією `(x, y)`
   - Застосувати колір (red/blue)
5. Зібрати всі рядки в `rich.text.Text` або `rich.console.Group`

### Фінал
- Коли всі об'єкти деактивовано (за межами екрану):
  - Поступово прибрати рамки дошки (fade out)
  - Очистити екран
  - Передати управління наступному ефекту (Result Banner)

### BoardLayout
- Допоміжний dataclass що зберігає координати клітинок та рамок на екрані
- Генерується рендерером на основі поточного розміру терміналу
- Використовується і для рендерингу, і для obstacles у фізиці

## Очікувані результати

- Після highlight (або одразу після game_over) — символи починають каскадно падати
- Кожен символ обертається під час падіння (зміна sprite кадрів)
- При зіткненні з рамкою — символ зміщується вбік і змінює напрямок обертання
- За кожним символом — затухаючий слід
- Після падіння всіх символів — екран очищується
- Анімація працює для будь-якого фінального стану дошки (1-9 символів)
- FPS стабільний, без помітних гальмувань

## Як тестувати виконання

```python
# test_falling.py
from tictactoe_cli.animations.falling import FallingSymbolsAnimation
from tic_tac_toe_3x3.logic.models import GameState, Grid

def test_all_objects_eventually_deactivate():
    """All falling objects should leave the screen."""
    state = GameState(Grid("XXX00    "))
    # Create animation with mock console
    # Fast-forward 200 frames
    # Assert all objects are inactive

def test_cascade_delay():
    """Objects should start falling at different times."""
    # Check that start_delays are different for each object
```

Візуальне тестування: довести гру до перемоги, спостерігати повну анімацію.

## Контрольні точки поза тестуванням

1. Каскад помітний — символи починають падати послідовно, а не одночасно
2. Обертання плавне — кадри змінюються без "стрибків"
3. Колізії працюють — символи не проходять крізь рамки
4. Сліди видні і затухають — додають динаміки
5. Анімація завершується за розумний час (3-5 секунд)
6. Працює коректно при різних розмірах терміналу (80x24, 120x40)
