# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта и устанавливаем зависимости
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev

# Копируем остальную часть приложения
COPY . .

# Указываем, что нужно копировать .env файл
COPY .env ./

# Устанавливаем команду для запуска FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]