FROM python:3.13-slim-bullseye

# Встановлюємо необхідні системні пакети
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Кешуємо встановлення бібліотек
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо лише код (завдяки .dockerignore це буде миттєво)
COPY . .

# Використовуємо стандартний порт Brawl Stars
EXPOSE 9339

# Запуск сервера
CMD ["python", "Main.py"]
