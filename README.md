# FastAPI Authorization

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.117.1-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.43-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supported-blue)
![Docker](https://img.shields.io/badge/Docker-Supported-blue)

## 📝 Описание проекта

Проект предоставляет REST API с системой аутентификации и авторизации пользователей. Приложение реализует регистрацию, вход, защиту маршрутов с использованием JWT токенов и предоставляет различные уровни доступа (обычный пользователь и администратор). Приложение поддерживает работу с PostgreSQL базой данных и может быть запущено как в контейнере Docker, так и локально.

## ✨ Особенности

- **Регистрация пользователей** - создание новых пользовательских аккаунтов
- **JWT токены** - безопасная аутентификация с помощью JSON Web Tokens
- **Защита маршрутов** - доступ к защищенным эндпоинтам только с действительным токеном
- **Ролевая система** - различный уровень доступа для обычных пользователей и администраторов
- **API документация** - автоматическая генерация Swagger UI и ReDoc документации
- **Docker поддержка** - возможность запуска в контейнерах с PostgreSQL

## 🛠️ Технологии

- **FastAPI** 0.17.1 - современный веб-фреймворк для создания API
- **SQLAlchemy** 2.0.43 - ORM для работы с базой данных
- **Pydantic** 2.11.9 - валидация данных
- **PostgreSQL** - основная база данных
- **AuthX** - библиотека для аутентификации и авторизации
- **Docker** - для контейнеризации

## 📁 Структура проекта

```
FastAPI_Authorization/
├── app/
│   ├── main.py                 # Основное приложение FastAPI
│   ├── database.py             # Настройки подключения к базе данных
│   ├── init_db.py              # Инициализация базы данных
│   ├── auth_config.py          # Конфигурация аутентификации и авторизации
│   ├── requirements.txt        # Зависимости проекта
│   ├── Dockerfile              # Docker конфигурация
│   ├── models/                 # Модели базы данных SQLAlchemy
│   │   ├── base.py
│   │   └── user.py
│   ├── schemas/                # Pydantic схемы для валидации данных
│   │   └── user.py             
│   ├── crud/                   # Операции CRUD для пользователей
│   │   └── user.py
│   └── routes/                 # API маршруты
│       └── user.py
├── docker-compose.yml          # Конфигурация Docker Compose
├── .env                        # Переменные окружения
├── .gitignore                  # Файлы, исключенные из Git
└── README.md                   # Документация проекта
```

## 🔧 Установка и запуск

### С использованием Docker (рекомендуется):

1. Клонируйте репозиторий:
```bash
git clone https://github.com/SergeyR-172/FastAPI_Authorization.git
cd FastAPI_Authorization
```

2. Создайте файл `.env` с настройками в репозиторий:
```bash
# Конфигурация базы данных
POSTGRES_USER=fastapi_user
POSTGRES_PASSWORD=fastapi_password
POSTGRES_DB=fastapi_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Конфигурация для приложения
DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
```

3. Запустите проект с помощью Docker Compose:
```bash
docker-compose up --build
```

Приложение будет доступно по адресу:
- API: `http://localhost:8000`
- API документация (Swagger): `http://localhost:8000/docs`
- ReDoc документация: `http://localhost:8000/redoc`

### Без Docker:

1. Клонируйте репозиторий:
```bash
git clone https://github.com/SergeyR-172/FastAPI_Authorization.git
cd FastAPI_Authorization
```

2. Установите зависимости:
```bash
pip install -r app/requirements.txt
```

3. Запустите инициализацию базы данных:
```bash
cd app
python init_db.py
```

4. Запустите приложение:
```bash
python main.py
```

Приложение будет доступно по адресу:
- API: `http://localhost:8000`
- API документация (Swagger): `http://localhost:8000/docs`
- ReDoc документация: `http://localhost:8000/redoc`

## 🌐 API эндпоинты

### Пользователи:
- `POST /register` - регистрация нового пользователя
- `POST /login` - вход в систему
- `GET /protected` - защищенный маршрут (требует токен)
- `GET /me` - получить информацию о текущем пользователе
- `GET /admin` - администраторский маршрут (требует токен администратора)

### Документация:
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

## 📋 Примеры использования API

### Регистрация пользователя:
```json
POST /register
{
  "username": "testuser",
  "password": "securepassword"
}
```

### Вход в систему:
```json
POST /login
{
  "username": "testuser",
  "password": "securepassword"
}
```
Ответ: JWT токен для дальнейшей аутентификации

### Доступ к защищенному маршруту:
```
GET /protected
Authorization: Bearer <your_jwt_token>
```

### Получение информации о текущем пользователе:
```
GET /me
Authorization: Bearer <your_jwt_token>
```

### Доступ к администраторскому маршруту:
```
GET /admin
Authorization: Bearer <admin_jwt_token>
```

## 🔐 Аутентификация и авторизация

### Регистрация
Пользователь может зарегистрироваться, отправив POST запрос на `/register` с именем пользователя и паролем. Пароль автоматически хешируется перед сохранением в базу данных.

### Вход
Пользователь может войти, отправив POST запрос на `/login` с именем пользователя и паролем. При успешной аутентификации возвращается JWT токен.

### Защита маршрутов
Для доступа к защищенным маршрутам необходимо включить JWT токен в заголовок Authorization: `Authorization: Bearer <token>`

### Ролевая система
Некоторые маршруты требуют прав администратора. Пользователь считается администратором, если у него установлен флаг `is_admin` в базе данных.

## 🗄️ База данных

Проект использует PostgreSQL для хранения данных пользователей. Структура базы данных включает:

- **users** - таблица пользователей
  - id: идентификатор пользователя
  - username: имя пользователя (уникальное)
  - hashed_password: хешированный пароль
  - is_admin: флаг администратора

## ℹ️ Дополнительная информация

- Приложение автоматически создает таблицы базы данных при запуске
- Все пароли хешируются перед сохранением
- JWT токены имеют ограниченное время жизни для безопасности
- Docker Compose автоматически запускает PostgreSQL и настраивает соединение
- Для администраторских прав установите `is_admin` в `true` в базе данных
