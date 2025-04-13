# FastAPI SQLAlchemy PostgreSQL SSL.

Приложение на `FastAPI` для изучения и демонстрации асинхронного взаимодействия с базой данных `PostgreSQL`.

Для развёртывания базы данных в режиме `SSL` используйте [эту инструкцию](https://github.com/SBRDIGITAL/postgrocker_ssl/).
SSL сертификаты для подключения к базе данных сохраните в `fastapi_sqlalchemy_postgresql_ssl/app/certs/`.

## Описание
Этот проект, который демонстрирует, как использовать `FastAPI` для создания асинхронного `API`, взаимодействующего с базой данных `PostgreSQL` и подключение к ней с помощью SSL сертификатов. В проекте реализован простой эндпоинт для получения информации о версии `PostgreSQL`.

## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/SBRDIGITAL/fastapi_sqlalchemy_postgresql_ssl.git
   cd fastapi_sqlalchemy_postgresql_ssl
   ```

2. **Создайте и активируйте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate     # Для Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

   Или, если вы используете `pyproject.toml`:
   ```bash
   pip install .
   ```

## Настройка базы данных
Перед запуском приложения убедитесь, что у вас есть доступ к базе данных PostgreSQL. Вам нужно будет настроить параметры подключения в файле `config_reader.py` (или в другом соответствующем файле конфигурации).

Пример строки подключения:
```python
DATABASE_URL_asyncpg_sslmode = "postgresql+asyncpg://user:password@localhost/dbname"
```
Замените `user`, `password`, `localhost` и `dbname` на ваши данные.

## Запуск приложения
Для запуска приложения используйте Uvicorn:
```bash
uvicorn app.main:app --reload
```
Замените `main` на имя вашего файла, если оно отличается.

## Использование
После запуска приложения вы можете получить информацию о версии PostgreSQL, отправив GET-запрос на следующий эндпоинт:
```
GET /postgres_version
```

Пример запроса с использованием `curl`:
```bash
curl http://127.0.0.1:8000/postgres_version
```