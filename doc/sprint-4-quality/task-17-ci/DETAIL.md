# Task 17 — CI: розширення та фіналізація: Детальний опис

## Мета
Розширити CI pipeline (створений в task-01 Sprint 1) coverage-звітністю, переконатися що повний набір тестів стабільно проходить, додати CI badge.

## Що робимо

1. Оновити `.github/workflows/ci.yml`:
   - Замінити `uv run pytest --tb=short -q` на `uv run pytest --tb=short --cov=tictactoe_cli --cov-report=term-missing`
   - Опціонально: додати upload coverage до Codecov або аналога
2. Додати CI badge в README
3. Перевірити що ai-reviewbot (з task-01) стабільно працює на реальних PR

## Як робимо

### Оновлення CI workflow
```yaml
      - name: Tests with coverage
        run: uv run pytest --tb=short --cov=tictactoe_cli --cov-report=term-missing

      # Опціонально: coverage upload
      - name: Upload coverage
        if: github.event_name == 'push'
        uses: codecov/codecov-action@v4
```

### CI Badge
```markdown
![CI](https://github.com/{owner}/{repo}/actions/workflows/ci.yml/badge.svg)
```

### Перевірка ai-reviewbot
- Створити тестовий PR з навмисною проблемою (unused import, type error)
- Переконатися що ai-reviewbot залишає релевантні inline-коментарі
- Налаштувати `LANGUAGE: uk` якщо потрібні українські коментарі

## Очікувані результати

- CI pipeline з coverage: `uv run pytest --cov` проходить, показує coverage > 70%
- CI badge в README — зелений
- ai-reviewbot стабільно ревьюїть PR (перевірено на 2-3 реальних PR)

## Як тестувати виконання

1. Push в main → Actions tab → ci.yml green, coverage виводиться в логах
2. Створити PR → ci.yml + ai-review.yml обидва проходять
3. ai-reviewbot залишає inline-коментарі на PR
4. Badge в README відображає актуальний статус

## Контрольні точки поза тестуванням

1. Coverage report видно в CI логах
2. Badge коректно оновлюється (green/red залежно від стану)
3. ai-reviewbot коментарі релевантні (не spam, не false positives на кожен рядок)
