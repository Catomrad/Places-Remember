# Используйте другой базовый образ Python
FROM python:3.11

# Установите рабочую директорию в контейнере
WORKDIR /app

# Скопируйте файлы проекта в контейнер
COPY . /app

# Установите зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Выполните миграции базы данных
RUN python manage.py migrate

# Откройте порт 8000 для доступа к приложению
EXPOSE 8000

# Запустите сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]