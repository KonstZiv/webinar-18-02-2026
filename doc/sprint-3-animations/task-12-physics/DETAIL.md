# Task 12 — 2D фізика: Детальний опис

## Мета
Створити простий 2D фізичний engine для симуляції падіння символів з гравітацією, колізіями та імпульсами.

## Що робимо

1. Створити `src/tictactoe_cli/animations/physics.py`
2. Dataclass `FallingObject` — стан падаючого об'єкта
3. Dataclass `Obstacle` — нерухома перепона (рамка дошки)
4. Клас `PhysicsEngine` — оновлення стану, детекція колізій
5. **Тести:** створити `tests/test_physics.py` — gravity, terminal velocity, collision detection, impulse, deactivation

## Як робимо

### FallingObject
```python
@dataclass
class FallingObject:
    x: float          # горизонтальна позиція (стовпець)
    y: float          # вертикальна позиція (рядок)
    vx: float = 0.0   # горизонтальна швидкість
    vy: float = 0.0   # вертикальна швидкість
    angle: int = 0     # поточний кадр обертання (індекс в sprite sheet)
    angular_vel: int = 0  # напрямок обертання (+1/-1)
    width: int = 17    # ширина спрайту
    height: int = 7    # висота спрайту
    active: bool = True  # чи ще на екрані
```

### Obstacle
```python
@dataclass(frozen=True)
class Obstacle:
    x: int
    y: int
    width: int
    height: int
```

### PhysicsEngine
```python
class PhysicsEngine:
    GRAVITY: float = 0.5       # прискорення вниз за кадр
    BOUNCE_IMPULSE: float = 2.0  # бічний імпульс при колізії
    TERMINAL_VY: float = 5.0    # максимальна швидкість падіння

    def __init__(self, obstacles: list[Obstacle], screen_height: int):
        self.obstacles = obstacles
        self.screen_height = screen_height

    def update(self, obj: FallingObject) -> None:
        """Update object position and velocity for one frame."""
        # 1. Apply gravity
        obj.vy = min(obj.vy + self.GRAVITY, self.TERMINAL_VY)
        # 2. Update position
        obj.x += obj.vx
        obj.y += obj.vy
        # 3. Check collisions
        self._resolve_collisions(obj)
        # 4. Update rotation
        obj.angle = (obj.angle + obj.angular_vel) % num_frames
        # 5. Deactivate if off screen
        if obj.y > self.screen_height:
            obj.active = False

    def _check_collision(self, obj: FallingObject, obs: Obstacle) -> bool:
        """AABB collision detection."""
        ...

    def _resolve_collisions(self, obj: FallingObject) -> None:
        """Resolve collisions with obstacles."""
        # Для кожної перепони:
        # 1. Detect overlap (AABB)
        # 2. Визначити сторону зіткнення
        # 3. Додати бічний імпульс (vx += або vx -=)
        # 4. Додати angular_velocity у напрямку зміщення
        ...
```

### Перепони
Рамки дошки — фіксовані позиції, відомі з рендерера:
- Горизонтальні рамки: верхня, 2 середні, нижня
- Вертикальні рамки: ліва, 2 середні, права
- Кожна рамка — `Obstacle(x, y, width=1або17, height=1або7)`

### Collision resolution
1. Detect: AABB overlap (bounding boxes перетинаються)
2. Визначити напрямок обходу:
   - Якщо об'єкт лівіше центру перепони → імпульс вліво
   - Якщо правіше → імпульс вправо
3. Додати `angular_vel` у напрямку бічного імпульсу (обертання у бік руху)
4. Скорегувати позицію щоб не "застряг" у перепоні

## Очікувані результати

- `FallingObject` при `update()` рухається вниз з прискоренням
- При зіткненні з `Obstacle` — зміщується вбік і починає обертатися
- Об'єкт деактивується коли виходить за нижню межу екрану
- Фізика стабільна — об'єкти не "застрягають" і не вилітають за межі

## Як тестувати виконання

```python
# test_physics.py
from tictactoe_cli.animations.physics import FallingObject, PhysicsEngine, Obstacle

def test_gravity():
    engine = PhysicsEngine(obstacles=[], screen_height=100)
    obj = FallingObject(x=10, y=0)
    engine.update(obj)
    assert obj.y > 0  # moved down
    assert obj.vy > 0  # has downward velocity

def test_terminal_velocity():
    engine = PhysicsEngine(obstacles=[], screen_height=1000)
    obj = FallingObject(x=10, y=0)
    for _ in range(100):
        engine.update(obj)
    assert obj.vy <= PhysicsEngine.TERMINAL_VY

def test_collision_gives_lateral_impulse():
    obstacle = Obstacle(x=10, y=20, width=17, height=1)
    engine = PhysicsEngine(obstacles=[obstacle], screen_height=100)
    obj = FallingObject(x=10, y=18, vy=2.0)
    engine.update(obj)
    assert obj.vx != 0  # got lateral impulse

def test_deactivation_off_screen():
    engine = PhysicsEngine(obstacles=[], screen_height=50)
    obj = FallingObject(x=10, y=51)
    engine.update(obj)
    assert not obj.active
```

## Контрольні точки поза тестуванням

1. Падіння виглядає природно — прискорення, не постійна швидкість
2. Об'єкти не проходять крізь перепони
3. Бічний імпульс візуально зрозумілий — об'єкт "обходить" перепону
4. Немає випадків "застрягання" об'єкта в циклі колізій
