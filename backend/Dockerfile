FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код бэкенда
COPY . .

# Команда запуска (используем run.py, который у вас есть)
CMD ["python", "run.py"]