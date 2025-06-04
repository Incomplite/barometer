# Barometer
## Установка

1. Клонирование репозитория

```bash
git clone https://github.com/Incomplite/barometer.git
```

2. Переход в директорию бота

```bash
cd barometer
```

3. Создание виртуального окружения

```bash
python3 -m venv .venv
```

4. Активация виртуального окружения

```bash
.venv/Scripts/activate
```

5. Установка зависимостей

```bash
pip3 install -r requirements.txt
```

6. Выполнение миграций Alembic

```bash
alembic upgrade head
```

7. Запуск проекта

```bash
python -m src.main
```
