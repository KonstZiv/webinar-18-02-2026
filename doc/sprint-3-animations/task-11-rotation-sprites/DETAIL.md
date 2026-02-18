# Task 11 — Спрайти обертання X/O: Детальний опис

## Мета
Створити sprite sheets для анімації обертання символів під час падіння. Кожен символ має набір кадрів, що імітують 3D обертання в 2D ASCII-арт.

## Що робимо

1. Створити `src/tictactoe_cli/animations/sprites.py`
2. Для символу X — мінімум 4 фази обертання (0°, 45°, 90°, 135°)
3. Для символу O — мінімум 4 фази обертання (коло → вертикальний еліпс → коло → горизонтальний еліпс)
4. API: `get_rotation_frames(mark: Mark) -> tuple[list[str], ...]`
5. **Тести:** створити `tests/test_sprites.py` — кількість кадрів, розміри, наявність блоків

## Як робимо

### Фази X (4+ кадри)
```
Фаза 0° (стандартний X):     Фаза 45° (|):
██           ██               ████████████████
 ███       ███                       ██
   ███   ███                         ██
     █████                           ██
   ███   ███                         ██
 ███       ███                       ██
██           ██               ████████████████

Фаза 90° (зворотній X):      Фаза 135° (—):
██           ██                      ██
  ███     ███                        ██
    ██   ██                          ██
     █████                    ████████████████
    ██   ██                          ██
  ███     ███                        ██
██           ██                      ██
```

### Фази O (4+ кадри)
```
Фаза 0° (коло):              Фаза 45° (вертикальний еліпс):
    █████████                      ███████
  ███       ███                   ██     ██
 ██           ██                  ██     ██
 ██           ██                  ██     ██
 ██           ██                  ██     ██
  ███       ███                   ██     ██
    █████████                      ███████

Фаза 90° (лінія):            Фаза 135° (горизонтальний еліпс):
                                █████████████
                               ██           ██
   █████████████               ██           ██
   █████████████
                               ██           ██
                               ██           ██
                                █████████████
```

### Формат даних
```python
X_FRAMES: tuple[list[str], ...] = (
    [...],  # frame 0 — 7 рядків по 17 символів
    [...],  # frame 1
    [...],  # frame 2
    [...],  # frame 3
)

O_FRAMES: tuple[list[str], ...] = (...)

def get_rotation_frames(mark: Mark) -> tuple[list[str], ...]:
    """Return rotation sprite frames for the given mark."""
    return X_FRAMES if mark is Mark.CROSS else O_FRAMES
```

### Принципи дизайну спрайтів
- Кожен кадр строго 17x7 символів (padding пробілами)
- Візуальна "маса" (кількість `█`) приблизно однакова між кадрами
- Перехід між сусідніми кадрами плавний — не занадто різкий стрибок
- Спрайти мають бути центровані в межах 17x7

## Очікувані результати

- `get_rotation_frames(Mark.CROSS)` → tuple з 4+ кадрів
- `get_rotation_frames(Mark.NAUGHT)` → tuple з 4+ кадрів
- Кожен кадр: `len(frame) == 7`, `len(line) == 17`
- При послідовному виводі кадрів — візуально зрозуміле обертання

## Як тестувати виконання

```python
# test_sprites.py
from tictactoe_cli.animations.sprites import get_rotation_frames
from tic_tac_toe_3x3.logic.models import Mark

@pytest.mark.parametrize("mark", [Mark.CROSS, Mark.NAUGHT])
def test_frame_count(mark):
    frames = get_rotation_frames(mark)
    assert len(frames) >= 4

@pytest.mark.parametrize("mark", [Mark.CROSS, Mark.NAUGHT])
def test_frame_dimensions(mark):
    for frame in get_rotation_frames(mark):
        assert len(frame) == 7
        assert all(len(line) == 17 for line in frame)

def test_frames_contain_blocks():
    for frame in get_rotation_frames(Mark.CROSS):
        assert any("█" in line for line in frame)
```

Візуальна перевірка:
```bash
uv run python -c "
import time
from tictactoe_cli.animations.sprites import get_rotation_frames
from tic_tac_toe_3x3.logic.models import Mark
for frame in get_rotation_frames(Mark.CROSS):
    print('\033[H\033[J')  # clear
    for line in frame:
        print(f'|{line}|')
    time.sleep(0.3)
"
```

## Контрольні точки поза тестуванням

1. Кожна фаза візуально відрізняється від попередньої
2. Послідовність кадрів створює враження обертання (а не випадкових форм)
3. Спрайти X та O мають різний характер обертання
4. Кадри циклічні: останній плавно переходить у перший
