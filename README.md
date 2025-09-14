# BlogApp - приложение на Python/FastAPI

## Описание проекта

Простой блог-сервер на Python/FastAPI с хранением данных в PostgreSQL.  
Приложение поддерживает два эндпоинта:

- **GET /posts** — возвращает список публикаций
- **POST /posts** — добавляет новую публикацию

Проект работает в Docker-контейнере и использует `docker-compose` для запуска приложения и БД одновременно.  
Логи приложения и БД сохраняются в папку `./logs`, данные PostgreSQL сохраняются между перезапусками контейнера через
volumes.



---

## Технологии

- Python 3.11
- FastAPI
- Uvicorn
- Logging
- SwaggerUI
- PostgreSQL
- Docker & Docker Compose
- GitHub Actions

---

## Структура проекта

```text
BlogApp/
├─ app/                               # Исходный код приложения
│  ├─ __init__.py
│  ├─ main.py                         # Точка входа FastAPI (инициализация приложения и маршрутов)
│  ├─ models.py                       # ORM‑модели SQLAlchemy
│  ├─ schemas.py                      # Pydantic‑схемы для запросов/ответов
│  ├─ crud.py                         # Бизнес‑логика и работа с БД
│  ├─ database.py                     # Инициализация сессий и Base
│  └─ logging_conf.py                 # Настройки логирования
│
├─ .github/
│  └─ workflows/
│     └─ deploy.yml                   # CI/CD workflow
│
├─ logs/                              # Точка монтирования для логов контейнеров
│  ├─ app/                            # Логи приложения
│  └─ postgres/                       # Логи PostgreSQL
│
├─ pgdata/                            # Данные PostgreSQL (volume), сохраняются между перезапусками
│  └─ ...
│
├─ Dockerfile                         
├─ docker-compose.yml                 
├─ requirements.txt                   
└─ README.md                          
```

---

## Локальная установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/ThreeToads/BlogApp
cd BlogApp
```

### 2. Создание .env файла

    # Пример данных для настройки PostgreSQL
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=tasks_db
    DB_HOST=db
    DB_PORT=5432

### 3. Сборка и запуск через Docker Compose

    docker-compose up --build

### Приложение будет доступно по адресам:

    http://localhost:8080/docs/
    http://127.0.0.1:8080/docs/

---

## Примеры запросов

Ниже показаны минимальные примеры с использованием curl и HTTPie. Адрес указывается для локального запуска по
умолчанию: `http://localhost:8080`.

### GET /posts — получить список публикаций

Запрос:

```bash
curl -s http://localhost:8080/posts
```

Пример ответа (200 OK):

```json
[
  {
    "id": 1,
    "title": "Первый пост",
    "content": "Пример содержимого"
  },
  {
    "id": 2,
    "title": "Второй пост",
    "content": "Еще один пример"
  }
]
```

### POST /posts — создать публикацию

Тело запроса (JSON):

```json
{
  "title": "Новый пост",
  "content": "Моё содержимое"
}
```

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"title":"Новый пост","content":"Моё содержимое"}' \
  http://localhost:8080/posts
```

```bash
http POST :8080/posts title="Новый пост" content="Моё содержимое"
```

Пример ответа (201 Created):

```json
{
  "id": 3,
  "title": "Новый пост",
  "content": "Моё содержимое"
}
```

Для интерактивного тестирования используйте Swagger UI по адресу `http://localhost:8080/docs`.

### Smoke-test

```bash
    curl http://localhost:8080/posts
    curl -X POST http://localhost:8080/posts -H "Content-Type: application/json" -d '{"title":"Test","content":"Test content"}'
```

### Auto Deploy

Проект настроен на деплой через GitHub Actions на сервер Railway

```
Настройки GitHub Secrets:
    RAILWAY_TOKEN
    DATABASE_URL
```

### Процесс деплоя

1. Push в ветку `main` запускает workflow GitHub Actions (`.github/workflows/deploy.yml`).
2. В пайплайне собирается Docker‑образ приложения и формируются артефакты для деплоя.
3. Аутентификация выполняется через секреты репозитория:
    - `RAILWAY_TOKEN` — для доступа к Railway (CLI/API)
    - `DATABASE_URL` — строка подключения к БД для приложения
4. Деплой выполняется на Railway, где сервис поднимается с помощью Docker.
5. Данные PostgreSQL сохраняются в volume `pgdata`; логи приложения и БД пишутся в каталог `/logs` на сервере.
6. Приложение работает по адресу: `https://blogapp-production-e309.up.railway.app/docs/`

