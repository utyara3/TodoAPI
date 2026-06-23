# ✅ TodoAPI

Простой REST API для управления задачами. Первый бэкенд-проект на FastAPI.

## ✨ Возможности

- CRUD операции для задач (создание, чтение, обновление, удаление)
- Асинхронная работа с SQLite через `aiosqlite`
- Валидация данных через Pydantic
- Автоматическая документация (Swagger UI)

## 🛠️ Технологии

- **FastAPI** — веб-фреймворк
- **aiosqlite** — асинхронный SQLite
- **Pydantic** — валидация данных
- **uv** — менеджер пакетов

## 🚀 Запуск

```bash
# Клонируем
git clone https://github.com/utyara3/TodoAPI.git
cd TodoAPI

# Устанавливаем зависимости
uv sync

# Создаём .env
echo "DB_PATH=todos.db" > .env

# Запускаем
uv run python main.py
```

API доступен на `http://localhost:8000`  
Документация: http://localhost:8000/docs

## 📡 Endpoints

- `GET /todos` — все задачи
- `GET /todos/{id}` — задача по ID
- `POST /todos` — создать задачу
- `PATCH /todos/{id}` — обновить задачу
- `DELETE /todos/{id}` — удалить задачу

## 📝 Лицензия

MIT
