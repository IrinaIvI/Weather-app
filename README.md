# Weather App

Это приложение на основе FastAPI для получения информации о погоде. Приложение интегрируется с внешними API для получения данных о погоде и использует асинхронный планировщик для периодических задач.

## Настройка проекта

Чтобы настроить проект локально, выполните следующие шаги:

### 1. Клонируйте репозиторий:

```bash
git clone https://github.com/IrinaIvI/Weather-app.git
cd Weather-app
```

### 2. Настройка окружения:

```bash
poetry config virtualenvs.in-project true
poetry shell
poetry install
```

### 3. Запуск сервера:

```bash
python src/app/main.py
```